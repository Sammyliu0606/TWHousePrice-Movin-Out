import pandas as pd
import os

# 定義縣市對應檔案與名稱
city_files = {
    "基隆市": "KL.csv",
    "新北市": "NT.csv",
    "台北市": "TP.csv",
    "桃園市": "TY.csv"
}

base_dir = "data/processed/HousePrice"
dfs = []

for city, filename in city_files.items():
    path = os.path.join(base_dir, filename)
    df = pd.read_csv(path, encoding="utf-8")
    # 新增「房屋單價（元/坪）」欄位
    df["房屋單價（元/坪）"] = df["房屋單價（元/平方公尺）"] * 3.306
    # 只保留需要的欄位
    df = df[["縣市", "鄉鎮市區", "房屋單價（元/坪）"]]
    dfs.append(df)

# 合併所有縣市
all_df = pd.concat(dfs, ignore_index=True)

# 計算每個縣市、每個鄉鎮市區的平均房屋單價（元/坪），四捨五入至小數點第二位
avg_df = (
    all_df.groupby(["縣市", "鄉鎮市區"], as_index=False)["房屋單價（元/坪）"]
    .mean()
    .round({"房屋單價（元/坪）": 2})
)

# 欄位名稱改為指定格式
avg_df = avg_df.rename(columns={"房屋單價（元/坪）": "4年來平均房屋單價（元/坪）"})

# 輸出為 utf-8 編碼的 csv
avg_df.to_csv("data/processed/HousePrice/all_cities_avg_house_price.csv", index=False, encoding="utf-8")

print(avg_df.head()) 

def merge_and_avg_house_price(base_dir, output_csv):
    # 定義縣市對應檔案與名稱
    city_files = {
        "基隆市": "KL.csv",
        "新北市": "NT.csv",
        "台北市": "TP.csv",
        "桃園市": "TY.csv"
    }

    dfs = []

    for city, filename in city_files.items():
        path = os.path.join(base_dir, filename)
        df = pd.read_csv(path, encoding="utf-8")
        # 新增「房屋單價（元/坪）」欄位
        df["房屋單價（元/坪）"] = df["房屋單價（元/平方公尺）"] * 3.306
        # 只保留需要的欄位
        df = df[["縣市", "鄉鎮市區", "房屋單價（元/坪）"]]
        dfs.append(df)

    # 合併所有縣市
    all_df = pd.concat(dfs, ignore_index=True)

    # 計算每個縣市、每個鄉鎮市區的平均房屋單價（元/坪），四捨五入至小數點第二位
    avg_df = (
        all_df.groupby(["縣市", "鄉鎮市區"], as_index=False)["房屋單價（元/坪）"]
        .mean()
        .round({"房屋單價（元/坪）": 2})
    )

    # 欄位名稱改為指定格式
    avg_df = avg_df.rename(columns={"房屋單價（元/坪）": "4年來平均房屋單價（元/坪）"})

    # 輸出為 utf-8 編碼的 csv
    avg_df.to_csv(output_csv, index=False, encoding="utf-8")
    return avg_df

def add_price_quartile_group(
    input_csv="data/processed/HousePrice/all_cities_avg_house_price.csv",
    output_csv="data/processed/HousePrice/all_cities_avg_house_price.csv"
):
    """
    讀取全縣市行政區平均房價csv，依據「4年來平均房屋單價（元/坪）」的四分位數(Q25, Q50, Q75)，
    新增「房價分群」欄位，分為「低房價」、「中低房價」、「中高房價」、「高房價」。
    結果覆蓋原csv或另存新檔。
    """
    df = pd.read_csv(input_csv, encoding="utf-8")
    price_col = "4年來平均房屋單價（元/坪）"

    # 計算四分位數
    q25 = df[price_col].quantile(0.25)
    q50 = df[price_col].quantile(0.50)
    q75 = df[price_col].quantile(0.75)

    # 定義分群函數
    def group_label(price):
        if price < q25:
            return "低房價"
        elif price < q50:
            return "中低房價"
        elif price < q75:
            return "中高房價"
        else:
            return "高房價"

    # 新增分群欄位
    df["房價分群"] = df[price_col].apply(group_label)

    # 輸出
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"已新增「房價分群」欄位並存檔至 {output_csv}")

if __name__ == "__main__":
    merge_and_avg_house_price(
        base_dir="data/processed/HousePrice",
        output_csv="data/processed/HousePrice/all_cities_avg_house_price.csv"
    )
    add_price_quartile_group() 