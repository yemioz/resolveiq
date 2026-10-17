"""
Kaplan-Meier estimation and log-rank testing utilities for
resolution-time survival curves.

The workflow supports:
- fitting separate Kaplan-Meier curves by agency, complaint type, or borough
- comparing survival distributions across groups with the multivariate log-rank test
- estimating survival probabilities at specified time horizons

Each fitted curve retains a group-specific label so downstream
reporting and visualization can distinguish survival profiles.

Log-rank tests evaluate whether survival distributions differ across
groups but do not, by themselves, identify which group performs
better or explain the cause of the difference.

Survival probabilities are obtained from the fitted step function,
including horizons that fall between observed event times.
"""

from __future__ import annotations

import pandas as pd
from lifelines import KaplanMeierFitter


def fit_km_by_group(
    df: pd.DataFrame,
    group_col: str,
    duration_col: str = "duration_days",
    event_col: str = "event_indicator",
) -> dict[str, KaplanMeierFitter]:
    """One fitted KaplanMeierFitter per distinct value of group_col."""
    raise NotImplementedError


def compare_groups_logrank(
    df: pd.DataFrame,
    group_col: str,
    duration_col: str = "duration_days",
    event_col: str = "event_indicator",
) -> dict:
    """Multivariate log-rank test across every level of group_col."""
    raise NotImplementedError


def survival_probability_at(kmf: KaplanMeierFitter, time_horizon: float) -> float:
    """P(duration > time_horizon) read off a fitted KM curve."""
    raise NotImplementedError
