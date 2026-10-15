"""
Transformer block: validation checks on the consolidated dataset.

Returns a dict of diagnostics instead of printing, so the orchestrator decides
how to report. Independent of how the data was produced.
"""
from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from utils.config import COLS
from utils.logging_config import get_logger

logger = get_logger(__name__)


def validate(df: pd.DataFrame) -> Dict[str, Any]:
    """Run completeness and sanity checks; return a diagnostics dict."""
    analytical_nulls = int(df[COLS].isnull().sum().sum())
    # annual values must be constant within a year
    const_ok = True
    for col in ["Total_Population", "Mobile_Subscriptions_Per100", "Internet_Users_Pct"]:
        per_year_unique = df.groupby("Year")[col].nunique()
        if (per_year_unique > 1).any():
            const_ok = False
    diagnostics = {
        "n_rows": len(df),
        "n_cols": df.shape[1],
        "analytical_nulls": analytical_nulls,
        "annual_values_constant_within_year": const_ok,
        "date_min": str(df["Date"].min().date()),
        "date_max": str(df["Date"].max().date()),
        "n_imputed_rows": int((df["Imputation_Flag"] != "").sum()),
    }
    logger.info("Validation: %d rows, %d analytical nulls, annual-constant=%s",
                diagnostics["n_rows"], analytical_nulls, const_ok)
    return diagnostics
