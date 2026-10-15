"""
Transformer block: merge indicators into one monthly frame.

Pure functions: outer-join the monthly economic series on Date, trim to the end
year, add Year/Month keys, then left-join the annual Social/Technological series
on Year. No I/O.
"""
from __future__ import annotations

from typing import Dict

import pandas as pd

from utils.config import END_YEAR, COLS
from utils.logging_config import get_logger

logger = get_logger(__name__)


def merge_monthly(monthly: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Outer-join the monthly economic frames on Date and sort by date."""
    frames = list(monthly.values())
    merged = frames[0].copy()
    for frame in frames[1:]:
        merged = merged.merge(frame, on="Date", how="outer")
    merged = merged.sort_values("Date").reset_index(drop=True)
    logger.info("Merged monthly frame: %d rows (%s to %s)", len(merged),
                merged["Date"].min().date(), merged["Date"].max().date())
    return merged


def trim_and_add_keys(monthly: pd.DataFrame, end_year: int = END_YEAR) -> pd.DataFrame:
    """Trim to end_year and insert Year and Month key columns."""
    out = monthly[monthly["Date"].dt.year <= end_year].reset_index(drop=True)
    out.insert(1, "Year", out["Date"].dt.year)
    out.insert(2, "Month", out["Date"].dt.month)
    logger.info("Trimmed to <=%d: %d rows", end_year, len(out))
    return out


def build_annual(annual: Dict[str, pd.DataFrame], end_year: int = END_YEAR) -> pd.DataFrame:
    """Merge the annual series on Year, derive Urban %, trim to end_year."""
    frames = list(annual.values())
    merged = frames[0]
    for frame in frames[1:]:
        merged = merged.merge(frame, on="Year", how="outer")
    merged["Urban_Pct_Population"] = (
        merged["Urban_Population"] / merged["Total_Population"] * 100
    )
    merged = merged[merged["Year"] <= end_year].reset_index(drop=True)
    logger.info("Annual table: %d years", len(merged))
    return merged


def join_annual_to_monthly(monthly: pd.DataFrame, annual: pd.DataFrame) -> pd.DataFrame:
    """Left-join annual values onto the monthly frame via Year and order columns."""
    df = monthly.merge(annual, on="Year", how="left")
    return df[COLS].copy()
