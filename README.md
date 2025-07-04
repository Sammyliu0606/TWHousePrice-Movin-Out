# TaiwanHousePrice-Movin&out

## 專案簡介
分析北北基桃各行政區房價如何影響人口在此大生活圈的遷移

## 目標
- 整理與分析北北基桃房價資料
- 研究房價變動對人口遷移的影響
- 視覺化趨勢與關聯

## 資料來源
- 內政部不動產交易實價登錄
- 政府公開資料平台 API

## 安裝與環境設置

```bash
# 建立資料夾結構
mkdir -p TaiwanHousePrice-MovinAndOut/{data/{raw,processed},notebooks,src,reports,tests}
cd TaiwanHousePrice-MovinAndOut

# 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 安裝套件
pip install -r requirements.txt
```

## 專案結構
```
TaiwanHousePrice-MovinAndOut/
├── data/
│   ├── raw/
│   │   ├── MovInOut/   # 各縣市月度淨遷移資料
│   │   └── Popu/       # 各縣市月度總人口資料
│   └── processed/
│       ├── MovInOut/   # 處理後的遷移率資料
│       └── HousePrice/ # 處理後的房價資料
├── notebooks/
├── src/
│   ├── process_mov_in_out.py      # 人口遷移資料處理腳本
│   └── process_house_price.py     # 房價資料處理與分群腳本
├── reports/
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

---

如需更細緻的腳本參數或 debug 說明，也可再補充！  
你可以直接將這段內容覆蓋或補充到你的 README.md。

---

## 人口遷移資料處理腳本說明（`src/process_mov_in_out.py`）

### 功能
- 處理 `data/raw/MovInOut/` 下的 KLnetmov.csv、NTnetmov.csv、TPnetmov.csv、TYnetmov.csv 及 `data/raw/Popu/` 下的 KLpopu.csv、NTpopu.csv、TPpopu.csv、TYpopu.csv。
- 產生 `data/processed/MovInOut/` 下的 KLmov.csv、NTmov.csv、TPmov.csv、TYmov.csv。
- 合併四縣市資料，產生 all_cities_mov.csv。
- 每個輸出檔案包含：
  - 行政區名稱
  - 4年總淨遷移（11001~11312月度加總）
  - 4年平均人口（11001~11312月度平均）
  - 4年淨遷移率（‰）：四捨五入至小數點第二位

### 執行方式

請在專案根目錄下執行：

```bash
python3 src/process_mov_in_out.py
```

---

## 房價資料處理與分群腳本說明（`src/process_house_price.py`）

### 功能
- 處理 `data/processed/HousePrice/` 下的 KL.csv、NT.csv、TP.csv、TY.csv。
- 將「房屋單價（元/平方公尺）」轉換為「房屋單價（元/坪）」。
- 針對每個縣市、每個鄉鎮市區，計算「房屋單價（元/坪）」的平均值，四捨五入至小數點第二位。
- 合併四縣市資料，產生 `all_cities_avg_house_price.csv`，結構如下：
  - 縣市
  - 鄉鎮市區
  - 4年來平均房屋單價（元/坪）
- 依據全體行政區平均房價的四分位數，新增「房價分群」欄位，分為：
  - 低房價（< Q25）
  - 中低房價（Q25 ~ Q50）
  - 中高房價（Q50 ~ Q75）
  - 高房價（> Q75）
- 最終輸出含分群的 `all_cities_avg_house_price.csv`。

### 執行方式

請在專案根目錄下執行：

```bash
python3 src/process_house_price.py
```

---

## 注意事項

- 輸入與輸出檔案皆為 UTF-8 編碼，逗號分隔。
- 若遇到欄位型態或資料對齊問題，請先檢查原始 csv 檔案格式與內容。

---

## 使用說明
- 請於 notebooks/ 進行資料探索與分析
- 共用程式碼請放於 src/
- 測試請放於 tests/ 