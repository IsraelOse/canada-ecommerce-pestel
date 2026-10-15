# Canada E-commerce PESTEL Analysis

A reproducible data pipeline that consolidates eight public macro indicators into a single **monthly PESTEL dataset** (2017–2025, 108 months) for the Canadian e-commerce market, with documented, transparent imputation. Delivered as a **modular, production-style pipeline** plus a companion analysis notebook and report.

## What it does
Loads, cleans, and merges indicators spanning three PESTEL dimensions:

- **Economic (monthly):** CPI (index, YoY, MoM), Consumer Confidence Index, Household Final Consumption Expenditure, retail e-commerce sales — *Statistics Canada, Conference Board of Canada*
- **Social (annual):** total population, urban population, derived urban share — *World Bank WDI*
- **Technological (annual):** mobile subscriptions per 100, internet users % — *World Bank / ITU*

Annual series are joined to the monthly grid by year. Two gaps are imputed and flagged:
- **HFCE (Jul–Dec 2025):** OLS regression on a time index + month dummies (trend + seasonality), **R² = 0.8488**.
- **Mobile & Internet (2025):** forward-fill from 2024, justified by near-saturation (flat) trends.

Output is a CSV and a formatted 4-sheet Excel workbook (Consolidated Dataset, Imputation Log, Variable Dictionary, Data Sources).

## Repository architecture
Decoupled, block-based layout — each block is a pure step that takes inputs and returns outputs.

```
.
├── data_loaders/        # Read the raw indicator Excel files
│   └── excel_loader.py
├── transformers/        # Pure merge, imputation, and validation logic
│   ├── consolidate.py
│   ├── imputation.py
│   └── validation.py
├── data_exporters/      # Write CSV + styled multi-sheet workbook
│   ├── local_exporter.py
│   └── workbook_content.py
├── utils/               # Shared config + structured logging
│   ├── config.py
│   └── logging_config.py
├── pipelines/
│   └── pestel_consolidation/
│       ├── run.py           # Orchestration
│       ├── metadata.yaml    # Execution order, variables, schedule
│       └── requirements.txt
├── PESTEL_Data_Pipeline.ipynb          # Analysis notebook (full narrative)
├── PESTEL_Analytical_Report.docx       # Written report
├── PESTEL_Presentation.pptx            # Slide deck
├── raw_indicators/                     # Source Excel files
└── outputs/                            # Generated dataset + workbook
```

Every block uses type hints and the standard `logging` module (no `print`), and loaders/transformers/exporters are fully decoupled.

## Run it
```bash
pip install -r pipelines/pestel_consolidation/requirements.txt
python -m pipelines.pestel_consolidation.run
```
Runs in a few seconds and writes `outputs/PESTEL_Monthly_Dataset.csv` and `.xlsx`.

## Verified
Running the pipeline reproduces the analysis exactly: 108 monthly rows, zero missing analytical values, HFCE OLS **R² = 0.8488**, and imputed HFCE values matching the report to the dollar (Jul 2025 = 1,686,672 … Dec 2025 = 1,718,841 CAD millions).

## Tech
Python · pandas · scikit-learn · openpyxl

*DAMO-501 Data Analytics Case Study, Master of Data Analytics, University of Niagara Falls Canada.*
