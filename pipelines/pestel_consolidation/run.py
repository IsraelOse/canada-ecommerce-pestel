"""
Pipeline orchestration: pestel_consolidation.

Wires the decoupled blocks:
    data_loaders -> transformers (consolidate -> impute -> flag -> validate)
    -> data_exporters
Run from the repository root:  python -m pipelines.pestel_consolidation.run
"""
from __future__ import annotations

import pandas as pd

from data_loaders.excel_loader import load_all_sources
from transformers.consolidate import (merge_monthly, trim_and_add_keys,
                                       build_annual, join_annual_to_monthly)
from transformers.imputation import (impute_hfce_ols, impute_annual_ffill,
                                      add_imputation_flags)
from transformers.validation import validate
from data_exporters.local_exporter import export_csv, export_workbook
from utils.config import END_YEAR
from utils.logging_config import get_logger

logger = get_logger("pipelines.pestel_consolidation")


def run() -> pd.DataFrame:
    """Execute the full consolidation pipeline and return the monthly dataset."""
    logger.info("=== pestel_consolidation pipeline start ===")

    monthly_src, annual_src = load_all_sources()

    monthly = trim_and_add_keys(merge_monthly(monthly_src))
    monthly, _ = impute_hfce_ols(monthly)

    annual = impute_annual_ffill(build_annual(annual_src), end_year=END_YEAR)

    df = join_annual_to_monthly(monthly, annual)
    df = add_imputation_flags(df, end_year=END_YEAR)

    diagnostics = validate(df)
    if diagnostics["analytical_nulls"] != 0:
        logger.warning("Dataset has %d null analytical values", diagnostics["analytical_nulls"])

    export_csv(df)
    export_workbook(df)
    logger.info("=== pipeline complete: %d rows, %d imputed ===",
                diagnostics["n_rows"], diagnostics["n_imputed_rows"])
    return df


if __name__ == "__main__":
    run()
