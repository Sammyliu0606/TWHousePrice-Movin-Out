# TaiwanHousePrice-Movin&out

## 專案簡介
分析北北基桃地區近五年房價漲跌與人口遷移之關聯。

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
uv venv .venv
source .venv/bin/activate

# 安裝套件
uv pip install -r requirements.txt
```

## 專案結構
```
TaiwanHousePrice-MovinAndOut/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── reports/
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## 使用說明
- 請於 notebooks/ 進行資料探索與分析
- 共用程式碼請放於 src/
- 測試請放於 tests/ 