import os
import pandas as pd

# 定義四個縣市的代碼與中文名稱
cities = {
    'KL': '基隆市',
    'NT': '新北市',
    'TP': '台北市',
    'TY': '桃園市'
}

# 設定原始資料與輸出資料的資料夾路徑
raw_mov_dir = os.path.join('..', 'data', 'raw', 'MovInOut')
raw_popu_dir = os.path.join('..', 'data', 'raw', 'Popu')
processed_dir = os.path.join('..', 'data', 'processed', 'MovInOut')
os.makedirs(processed_dir, exist_ok=True)

def merge_all_city_mov_data(output_csv=None):
    """
    合併 processed_dir 內四個縣市的 mov.csv，插入「縣市」欄位，
    並將第一欄表頭名稱改為「行政區」。
    若 output_csv 給定，則輸出合併後的 csv。
    """
    city_files = {
        '基隆市': 'KLmov.csv',
        '新北市': 'NTmov.csv',
        '台北市': 'TPmov.csv',
        '桃園市': 'TYmov.csv'
    }
    dfs = []
    for city, filename in city_files.items():
        path = os.path.join(processed_dir, filename)
        df = pd.read_csv(path, encoding="utf-8")
        # 插入「縣市」欄位於第0欄
        df.insert(0, "縣市", city)
        # 將原本第一欄表頭名稱改為「行政區」
        old_area_col = df.columns[1]
        df = df.rename(columns={old_area_col: "行政區"})
        dfs.append(df)
    all_df = pd.concat(dfs, ignore_index=True)
    if output_csv:
        all_df.to_csv(output_csv, index=False, encoding="utf-8")
    return all_df

for city_code in cities.keys():
    print(f"處理 {city_code} ...")
    # 1. 讀取淨遷移資料
    mov_file = f"{city_code}netmov.csv"
    mov_path = os.path.join(raw_mov_dir, mov_file)
    print(f"讀取 {mov_path}")
    mov_df = pd.read_csv(mov_path, encoding="utf-8")
    
    # 2. 刪除10912欄位
    if "10912" in mov_df.columns:
        mov_df = mov_df.drop(columns=["10912"])
    
    # 3. 讀取人口資料
    popu_file = f"{city_code}popu.csv"
    popu_df = pd.read_csv(os.path.join(raw_popu_dir, popu_file), encoding="utf-8")

    # 轉數值
    mov_months = [col for col in mov_df.columns if col.isdigit() and 11001 <= int(col) <= 11312]
    for col in mov_months:
        mov_df[col] = pd.to_numeric(mov_df[col], errors='coerce')
    
    # 4. 計算4年平均人口（11001~11312）
    # 只取11001~11312這48個月的欄位
    popu_months = [col for col in popu_df.columns if col.isdigit() and 11001 <= int(col) <= 11312]
    popu_df["4年平均人口"] = popu_df[popu_months].mean(axis=1)
    
    # 5. 計算4年總淨遷移（11001~11312）
    mov_months = [col for col in mov_df.columns if col.isdigit() and 11001 <= int(col) <= 11312]
    mov_df["4年總淨遷移"] = mov_df[mov_months].sum(axis=1)

    print("4年總淨遷移（前5行）:")
    print(mov_df[["4年總淨遷移"]].head())
    print("4年平均人口（前5行）:")
    print(popu_df[["4年平均人口"]].head())
    
    # 取行政區名稱欄位名稱
    area_col = mov_df.columns[0]
    mov_df[area_col] = mov_df[area_col].str.strip()
    popu_df[area_col] = popu_df[area_col].str.strip()

    # 只保留行政區名稱和4年總淨遷移
    mov_simple = mov_df[[area_col, "4年總淨遷移"]].copy()
    popu_simple = popu_df[[area_col, "4年平均人口"]].copy()

    # 以行政區名稱合併
    result = pd.merge(mov_simple, popu_simple, on=area_col, how="left")

    # 計算4年淨遷移率
    result["4年淨遷移率（‰）"] = (result["4年總淨遷移"] / result["4年平均人口"] * 1000).round(2)

    print("合併後結果（前5行）:")
    print(result.head())
    
    # 8. 輸出到 processed/MovInOut
    out_file = f"{city_code}mov.csv"
    out_path = os.path.join(processed_dir, out_file)
    print(f"輸出 {out_path}")
    result.to_csv(out_path, index=False, encoding="utf-8")

if __name__ == "__main__":
    # 產生合併後的 dataframe 並存檔
    merged_df = merge_all_city_mov_data(output_csv=os.path.join(processed_dir, "all_cities_mov.csv"))
    print(merged_df.head())