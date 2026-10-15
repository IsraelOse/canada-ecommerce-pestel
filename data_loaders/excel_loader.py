"""
Data loader block: read the raw indicator Excel files.

Pure acquisition: each function reads one workbook and returns a tidy DataFrame.
Knows nothing about merging, imputation, or export.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import openpyxl
import pandas as pd

from utils.config import RAW_DIR, MONTHLY_SOURCES, ANNUAL_SOURCES
from utils.logging_config import get_logger

logger = get_logger(__name__)


def load_monthly(filename: str, rename: Optional[Dict[str, str]] = None,
                 data_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Load a monthly Excel source into a DataFrame with a parsed Date column.

    Cleaning: drops columns with empty headers (export artefacts) and converts
    comma-formatted strings such as '5,024,757' to float.
    """
    wb = openpyxl.load_workbook(Path(data_dir) / filename, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    headers = list(rows[0])
    records: List[dict] = []
    for r in rows[1:]:
        record = {}
        for i, header in enumerate(headers):
            if header is None:
                continue
            value = r[i]
            if isinstance(value, str):
                try:
                    value = float(value.replace(",", ""))
                except ValueError:
                    pass
            record[header] = value
        records.append(record)
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    return df.rename(columns=rename) if rename else df


def load_annual(filename: str, value_col: str,
                data_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Load an annual Excel file (first two columns: Year, Value)."""
    wb = openpyxl.load_workbook(Path(data_dir) / filename, data_only=True)
    ws = wb.active
    records: List[dict] = []
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if r[0] is None:
            continue
        try:
            year = int(str(r[0]))
        except ValueError:
            year = r[0]
        records.append({"Year": year, value_col: r[1]})
    return pd.DataFrame(records)


def load_all_sources() -> Tuple[Dict[str, pd.DataFrame], Dict[str, pd.DataFrame]]:
    """Load every configured monthly and annual source.

    Returns (monthly_frames, annual_frames) keyed by a short name.
    """
    monthly = {fname: load_monthly(fname, rename) for fname, rename in MONTHLY_SOURCES.items()}
    annual = {value_col: load_annual(fname, value_col) for fname, value_col in ANNUAL_SOURCES}
    logger.info("Loaded %d monthly and %d annual source files",
                len(monthly), len(annual))
    return monthly, annual
