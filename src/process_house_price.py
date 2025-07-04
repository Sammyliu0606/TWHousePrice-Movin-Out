import os
import glob
import pandas as pd
import sys

def main():
    # 1. 命令列參數處理
    if len(sys.argv) != 2:
        print("使用方式: python merge_clean_KL.py [城市代碼]")
        print("支援的城市代碼: KL (基隆市), NT (新北市), TP (台北市), TY (桃園市)")
        print("範例: python merge_clean_KL.py KL")
        sys.exit(1)
    
    city_code = sys.argv[1].upper()
    
    # 2. 城市名稱對應表
    city_names = {
        'KL': '基隆市',
        'NT': '新北市',
        'TP': '台北市',
        'TY': '桃園市'
    }
    
    if city_code not in city_names:
        print(f"錯誤: 不支援的城市代碼 '{city_code}'")
        print("支援的城市代碼: KL, NT, TP, TY")
        sys.exit(1)
    
    print(f"開始處理 {city_names[city_code]} ({city_code}) 的資料...")
    
    # 3. 動態路徑設定
    raw_dir = os.path.join('..', 'data', 'raw', 'HousePrice', city_code)
    processed_dir = os.path.join('..', 'data', 'processed', 'HousePrice')
    os.makedirs(processed_dir, exist_ok=True)
    
    # 檢查原始資料夾是否存在
    if not os.path.exists(raw_dir):
        print(f"錯誤: 找不到資料夾 {raw_dir}")
        sys.exit(1)
    
    # 4. 讀取所有檔案
    city_files = glob.glob(os.path.join(raw_dir, f'{city_code}*.csv'))
    cityp_files = glob.glob(os.path.join(raw_dir, f'{city_code}p*.csv'))
    
    frames = []
    for f in city_files + cityp_files:
        try:
            df = pd.read_csv(f, encoding='utf-8')
            # 刪除第二列英文表頭
            if df.shape[0] > 1 and 'The villages and towns urban district' in str(df.iloc[0].values):
                df = df.drop(index=0).reset_index(drop=True)
            # 只合併有資料的dataframe
            if df.shape[0] == 0:
                continue
            # 標註資料來源
            df['資料來源'] = '成屋' if os.path.basename(f).startswith(city_code) and not os.path.basename(f).startswith(f'{city_code}p') else '預售屋'
            frames.append(df)
        except Exception as e:
            print(f'檔案 {f} 讀取失敗: {e}')
    
    if not frames:
        print('無可用資料，結束處理')
        sys.exit(1)
    
    # 5. 欄位統一
    all_columns = set()
    for df in frames:
        all_columns.update(df.columns)
    all_columns = list(all_columns)
    frames = [df.reindex(columns=all_columns) for df in frames]
    
    # 6. 合併
    all_df = pd.concat(frames, ignore_index=True)
    print(f'合併前資料筆數: {all_df.shape[0]}')
    
    # 7. 只保留交易標的為指定值
    all_df = all_df[all_df['交易標的'].isin(['房地(土地+建物)', '房地(土地+建物)+車位'])]
    print(f'交易標的篩選後資料筆數: {all_df.shape[0]}')
    
    # 8. 欄位篩選
    keep_cols = [
        '鄉鎮市區',
        '交易年月日',
        '建物移轉總面積平方公尺',
        '總價元',
        '車位總價元',
        '資料來源'
    ]
    all_df = all_df[keep_cols]
    
    # 9. 刪除重複
    all_df = all_df.drop_duplicates()
    print(f'去除重複後資料筆數: {all_df.shape[0]}')
    
    # 10. 交易年月日篩選
    all_df = all_df[all_df['交易年月日'].astype(str).str.isnumeric()]
    all_df['交易年月日'] = all_df['交易年月日'].astype(int)
    all_df = all_df[(all_df['交易年月日'] >= 1100101) & (all_df['交易年月日'] <= 1131231)]
    print(f'日期篩選後資料筆數: {all_df.shape[0]}')
    
    # 11. 缺失值處理
    all_df['車位總價元'] = all_df['車位總價元'].fillna(0)
    
    # 12. 過濾異常值
    all_df['建物移轉總面積平方公尺'] = pd.to_numeric(all_df['建物移轉總面積平方公尺'], errors='coerce')
    all_df['總價元'] = pd.to_numeric(all_df['總價元'], errors='coerce')
    all_df['車位總價元'] = pd.to_numeric(all_df['車位總價元'], errors='coerce')
    all_df = all_df[(all_df['建物移轉總面積平方公尺'] > 0) & (all_df['總價元'] > 0)]
    print(f'異常值過濾後資料筆數: {all_df.shape[0]}')
    
    # 13. 新增欄位
    all_df['縣市'] = city_names[city_code]
    all_df['房屋單價（元/平方公尺）'] = (all_df['總價元'] - all_df['車位總價元']) / all_df['建物移轉總面積平方公尺']
    
    # 14. 輸出統計
    print(f'\n{city_names[city_code]} 最終資料基本統計：')
    print(all_df.describe(include='all'))
    
    # 15. 輸出CSV
    output_path = os.path.join(processed_dir, f'{city_code}.csv')
    all_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'已儲存至 {output_path}')

if __name__ == "__main__":
    main() 