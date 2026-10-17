"""
Logistic regression baseline for predicting whether a request is
resolved within its service-level agreement (SLA).

The baseline provides a point-in-time classification probability that
can be compared with survival-model estimates of remaining open beyond
the SLA horizon.

The workflow supports:
- preprocessing categorical and numeric covariates
- one-hot encoding categorical features while tolerating unseen
  categories at inference time
- fitting a logistic regression classifier
- constructing the binary resolved-within-SLA target

Still-open requests that have already exceeded the SLA are treated as
not resolved within SLA. Requests that remain open but have not yet
reached the SLA horizon require explicit handling because their final
outcome is not yet observed.
"""

from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_pipeline(categorical_cols: list[str], numeric_cols: list[str]) -> Pipeline:
    raise NotImplementedError


def make_target(
    df: pd.DataFrame,
    sla_days: int,
    duration_col: str = "duration_days",
    event_col: str = "event_indicator",
) -> pd.Series:
    raise NotImplementedError
