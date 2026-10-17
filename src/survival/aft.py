"""
Parametric accelerated failure time (AFT) modeling utilities.

AFT models provide an alternative survival-modeling approach when
the proportional-hazards assumption is not appropriate for one or
more covariates.

Supported candidate models:
- Weibull AFT
- Log-normal AFT
- Log-logistic AFT

Candidate models are fit on the same analysis dataset so their AIC
values are directly comparable. The model with the lowest AIC is
selected.

Survival prediction uses a common interface with the Cox PH scoring
workflow so downstream code can score either model type consistently.
"""
# Candidate AFT models must be fit using the same rows, covariates,
# duration column, and event indicator for valid AIC comparison.

from __future__ import annotations

import pandas as pd
from lifelines import LogLogisticAFTFitter, LogNormalAFTFitter, WeibullAFTFitter

AFT_MODELS = {
    "weibull": WeibullAFTFitter,
    "lognormal": LogNormalAFTFitter,
    "loglogistic": LogLogisticAFTFitter,
}


def fit_aft_candidates(
    df: pd.DataFrame,
    covariates: list[str],
    duration_col: str = "duration_days",
    event_col: str = "event_indicator",
) -> dict[str, object]:
    """Fit all three AFT candidates on the same data."""
    raise NotImplementedError


def select_best_by_aic(fitted_models: dict[str, object]) -> tuple[str, object]:
    """Return (name, model) of the lowest-AIC candidate."""
    raise NotImplementedError


def predict_survival_at(model, X: pd.DataFrame, time_horizon: float) -> pd.Series:
    """Same interface as cox_ph.predict_survival_at."""
    raise NotImplementedError
