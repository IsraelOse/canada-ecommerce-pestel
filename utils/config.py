"""
Central configuration for the Canada E-commerce PESTEL consolidation pipeline.

Holds source-file paths, the column rename maps for each raw indicator, the
final column order, and output locations. No block hard-codes these.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

ROOT: Path = Path(__file__).resolve().parents[1]
RAW_DIR: Path = ROOT / "raw_indicators"
OUTPUTS: Path = ROOT / "outputs"
CSV_OUT: Path = OUTPUTS / "PESTEL_Monthly_Dataset.csv"
XLSX_OUT: Path = OUTPUTS / "PESTEL_Monthly_Dataset.xlsx"

END_YEAR: int = 2025  # keep observations up to and including this year

# Monthly economic sources: filename -> {raw column: clean name}
MONTHLY_SOURCES: Dict[str, Dict[str, str]] = {
    "CPI.xlsx": {
        "Total CPI (seasonally adjusted)": "CPI_Index",
        "Total CPI, percentage change year-over-year (unadjusted)": "CPI_YoY_Pct",
        "Total CPI, percentage change month-over-month": "CPI_MoM_Pct",
    },
    "Consumer confidence index (CCI).xlsx": {
        "Consumer confidence index (CCI)": "Consumer_Confidence_Index",
    },
    "Household final consumption expenditure(millions).xlsx": {
        "Household final consumption expenditure(millions)": "HFCE_Millions",
    },
    "Retail e commerce sales 2017-26.xlsx": {
        "Dollars(x1000)": "Ecommerce_Sales_000s",
    },
}

# Annual sources: (filename, value column name)
ANNUAL_SOURCES: List[Tuple[str, str]] = [
    ("Population, total.xlsx", "Total_Population"),
    ("Urban population.xlsx", "Urban_Population"),
    ("Mobile cellular subscriptions (per 100 people).xlsx", "Mobile_Subscriptions_Per100"),
    ("Individuals using the Internet (% of population).xlsx", "Internet_Users_Pct"),
]

# Final column order: Key -> Economic -> Social -> Technological
COLS: List[str] = [
    "Date", "Year", "Month",
    "CPI_Index", "CPI_YoY_Pct", "CPI_MoM_Pct",
    "Consumer_Confidence_Index", "HFCE_Millions", "Ecommerce_Sales_000s",
    "Total_Population", "Urban_Population", "Urban_Pct_Population",
    "Mobile_Subscriptions_Per100", "Internet_Users_Pct",
]

# PESTEL component of each column (used for styling + the data dictionary)
PESTEL_MAP: Dict[str, str] = {
    **{c: "Economic" for c in ["CPI_Index", "CPI_YoY_Pct", "CPI_MoM_Pct",
                               "Consumer_Confidence_Index", "HFCE_Millions",
                               "Ecommerce_Sales_000s"]},
    **{c: "Social" for c in ["Total_Population", "Urban_Population", "Urban_Pct_Population"]},
    **{c: "Technological" for c in ["Mobile_Subscriptions_Per100", "Internet_Users_Pct"]},
    **{c: "Key" for c in ["Date", "Year", "Month"]},
    "Imputation_Flag": "Note",
}
