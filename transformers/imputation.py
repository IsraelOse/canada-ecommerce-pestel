"""
Transformer block: impute the two kinds of missing values.

- HFCE (monthly) is observed to mid-2025; the tail is imputed with an OLS model
  on a time index plus month dummies (trend + seasonality).
- Annual technological indicators run to 2024 and are forward-filled to 2025,
  justified by their near-saturation (flat) trend.
"""
from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from utils.logging_config import get_logger

logger = get_logger(__name__)


def impute_hfce_ols(monthly: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
    """Impute missing HFCE_Millions with OLS (time index + month dummies).

    Returns the frame with HFCE filled and the training R^2.
    """
    out = monthly.copy()
    train = out[out["HFCE_Millions"].notnull()].copy()
    train["t"] = np.arange(len(train))
    dummies_train = pd.get_dummies(train["Month"], prefix="m", drop_first=True).astype(float)
    X_train = pd.concat([train[["t"]], dummies_train], axis=1)
    model = LinearRegression().fit(X_train, train["HFCE_Millions"])
    r2 = float(model.score(X_train, train["HFCE_Millions"]))

    missing = out[out["HFCE_Millions"].isnull()].copy()
    if not missing.empty:
        missing["t"] = np.arange(len(train), len(train) + len(missing))
        dummies_pred = (pd.get_dummies(missing["Month"], prefix="m")
                        .reindex(columns=dummies_train.columns, fill_value=0)
                        .astype(float))
        X_pred = pd.concat([missing[["t"]], dummies_pred], axis=1)
        out.loc[out["HFCE_Millions"].isnull(), "HFCE_Millions"] = model.predict(X_pred)
    logger.info("HFCE OLS imputation: R2=%.4f, intercept=%.0f, trend=+%.0f/month, %d rows imputed",
                r2, model.intercept_, model.coef_[0], len(missing))
    return out, r2


def impute_annual_ffill(annual: pd.DataFrame, end_year: int = 2025,
                        cols=("Mobile_Subscriptions_Per100", "Internet_Users_Pct")) -> pd.DataFrame:
    """Forward-fill the final year of the given annual columns from the prior year."""
    out = annual.copy()
    for col in cols:
        prev = out.loc[out["Year"] == end_year - 1, col].values
        if len(prev):
            out.loc[out["Year"] == end_year, col] = prev[0]
            logger.info("Forward-filled %s for %d <- %.4f", col, end_year, prev[0])
    return out


def add_imputation_flags(df: pd.DataFrame, end_year: int = 2025) -> pd.DataFrame:
    """Add a per-row Imputation_Flag describing any imputation applied."""
    out = df.copy()
    out["Imputation_Flag"] = ""
    out.loc[(out["Year"] == end_year) & (out["Month"] >= 7), "Imputation_Flag"] = \
        "HFCE: OLS regression (trend + seasonal dummies)"
    mask = out["Year"] == end_year
    out.loc[mask, "Imputation_Flag"] = out.loc[mask, "Imputation_Flag"].apply(
        lambda x: (x + "; " if x else "") + "Mobile & Internet: forward fill from 2024")
    return out
