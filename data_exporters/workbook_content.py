"""
Static documentation content for the exported workbook: the imputation log,
variable dictionary, and data-source register. Kept as data so the exporter
stays focused on formatting.
"""
from __future__ import annotations

from typing import List

IMPUTATION_LOG: List[list] = [
    ["HFCE_Millions", "Economic", "Jul-Dec 2025", "6", "OLS Regression",
     "Source ends Jun 2025; 6 months imputed using OLS with a time index plus "
     "month dummies to capture trend and seasonality.",
     "HFCE ~ t + month_dummies (Feb-Dec); n=102; R2=0.8488; sklearn LinearRegression",
     "Jul:1,686,672 | Aug:1,695,758 | Sep:1,702,521 | Oct:1,708,236 | "
     "Nov:1,713,388 | Dec:1,718,841 (CAD millions)"],
    ["Mobile_Subscriptions_Per100", "Technological", "All 2025", "12", "Forward Fill",
     "ITU data only through 2024. Near saturation (87-94/100 since 2019); flat trend.",
     "Carry-forward: 2025 <- 2024 observed value (94.1060). No model fitted.",
     "2025: 94.1060 per 100 people (all 12 months inherit via Year join)"],
    ["Internet_Users_Pct", "Technological", "All 2025", "12", "Forward Fill",
     "ITU data only through 2024. >93% penetration since 2021; annual change <0.5pp.",
     "Carry-forward: 2025 <- 2024 observed value (94.3533). No model fitted.",
     "2025: 94.3533% of population (all 12 months inherit via Year join)"],
]

VARIABLE_DICTIONARY: List[list] = [
    ["Date", "Key", "Calendar month start date (YYYY-MM-DD)", "Date", "Monthly",
     "Derived from source files", "2017-01 to 2025-12", "None"],
    ["Year", "Key", "Calendar year; join key for annual variables", "Integer", "Monthly",
     "Derived from Date", "2017 to 2025", "None"],
    ["Month", "Key", "Month number (1=Jan, 12=Dec)", "Integer", "Monthly",
     "Derived from Date", "1 to 12", "None"],
    ["CPI_Index", "Economic", "Consumer Price Index, all-items, seasonally adjusted",
     "Index (2002=100)", "Monthly", "Statistics Canada 18-10-0004-01", "2017-01 to 2025-12", "None"],
    ["CPI_YoY_Pct", "Economic", "CPI year-over-year % change (unadjusted)", "%", "Monthly",
     "Statistics Canada 18-10-0004-01", "2017-01 to 2025-12", "None"],
    ["CPI_MoM_Pct", "Economic", "CPI month-over-month % change", "%", "Monthly",
     "Statistics Canada 18-10-0004-01", "2017-01 to 2025-12", "None"],
    ["Consumer_Confidence_Index", "Economic", "Conference Board of Canada CCI (1985=100)",
     "Index (1985=100)", "Monthly", "Conference Board of Canada", "2017-01 to 2025-12", "None"],
    ["HFCE_Millions", "Economic", "Household Final Consumption Expenditure",
     "CAD Millions", "Monthly", "Statistics Canada 36-10-0107-01", "2017-01 to 2025-12",
     "Jul-Dec 2025: OLS regression (R2=0.85)"],
    ["Ecommerce_Sales_000s", "Economic", "Monthly retail e-commerce sales in Canada",
     "CAD Thousands", "Monthly", "Statistics Canada 20-10-0072-01", "2017-01 to 2025-12", "None"],
    ["Total_Population", "Social", "Total resident population of Canada", "Persons",
     "Annual to Monthly", "World Bank WDI SP.POP.TOTL", "2017 to 2025", "None"],
    ["Urban_Population", "Social", "Population in urban areas", "Persons",
     "Annual to Monthly", "World Bank WDI SP.URB.TOTL", "2017 to 2025", "None"],
    ["Urban_Pct_Population", "Social", "Derived: Urban/Total x 100", "%",
     "Annual to Monthly", "Derived from WDI", "2017 to 2025", "None"],
    ["Mobile_Subscriptions_Per100", "Technological", "Mobile subscriptions per 100 people",
     "Per 100 people", "Annual to Monthly", "World Bank/ITU IT.CEL.SETS.P2", "2017 to 2024",
     "2025: Forward fill (94.1060)"],
    ["Internet_Users_Pct", "Technological", "Individuals using the Internet",
     "% of population", "Annual to Monthly", "World Bank/ITU IT.NET.USER.ZS", "2017 to 2024",
     ">93% since 2021; 2025: Forward fill (94.3533%)"],
    ["Imputation_Flag", "Note", "Describes imputation applied to this row; empty if observed",
     "Text", "Monthly", "Derived", "2017-01 to 2025-12", "N/A"],
]

DATA_SOURCES: List[list] = [
    ["Economic", "CPI_Index, CPI_YoY_Pct, CPI_MoM_Pct", "CPI monthly (seasonally adj.)",
     "Statistics Canada", "18-10-0004-01",
     "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810000401", "Monthly", "2017-01 to 2025-12"],
    ["Economic", "Consumer_Confidence_Index", "Consumer Confidence Index",
     "Conference Board of Canada", "CCI Monthly",
     "https://www.conferenceboard.ca/", "Monthly", "2017-01 to 2025-12"],
    ["Economic", "HFCE_Millions", "Household Final Consumption Expenditure",
     "Statistics Canada", "36-10-0107-01",
     "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610010701", "Monthly",
     "2017-01 to 2025-06 obs; Jul-Dec 2025 imputed"],
    ["Economic", "Ecommerce_Sales_000s", "Retail e-commerce sales, Canada",
     "Statistics Canada", "20-10-0072-01",
     "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2010007201", "Monthly", "2017-01 to 2025-12"],
    ["Social", "Total_Population", "Population, total - Canada", "World Bank WDI",
     "SP.POP.TOTL", "https://data.worldbank.org/indicator/SP.POP.TOTL?locations=CA", "Annual", "2017 to 2025"],
    ["Social", "Urban_Population", "Urban population - Canada", "World Bank WDI",
     "SP.URB.TOTL", "https://data.worldbank.org/indicator/SP.URB.TOTL?locations=CA", "Annual", "2017 to 2025"],
    ["Social", "Urban_Pct_Population (derived)", "Computed: Urban/Total x 100", "Derived",
     "N/A", "N/A", "Annual", "2017 to 2025"],
    ["Technological", "Mobile_Subscriptions_Per100", "Mobile subscriptions per 100",
     "World Bank / ITU", "IT.CEL.SETS.P2",
     "https://data.worldbank.org/indicator/IT.CEL.SETS.P2?locations=CA", "Annual", "2017-2024 obs; 2025 fwd-fill"],
    ["Technological", "Internet_Users_Pct", "Internet users % of population",
     "World Bank / ITU", "IT.NET.USER.ZS",
     "https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=CA", "Annual", "2017-2024 obs; 2025 fwd-fill"],
]
