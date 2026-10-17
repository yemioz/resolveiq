"""
Point-in-time feature engineering utilities.

All generated features must satisfy the temporal constraint:

    feature_information_timestamp <= prediction_timestamp

Historical aggregates are computed using only information available
before each request's own created_date.

The module supports:
- calendar features derived from request intake timestamps
- trailing median duration features over configurable historical windows
- open caseload at intake for the relevant grouping level

Trailing aggregates exclude the current observation to prevent target
leakage. Rows with no prior eligible history are handled explicitly.

Open-caseload features represent requests that were already created
and not yet closed at the prediction timestamp. These values may be
derived from precomputed backlog tables when available.
"""

from __future__ import annotations

import pandas as pd


def add_calendar_features(df: pd.DataFrame, created_col: str = "created_date") -> pd.DataFrame:
    """Hour/day-of-week/month features derived purely from intake time."""
    raise NotImplementedError


def add_trailing_median_duration(
    df: pd.DataFrame,
    group_cols: list[str],
    window: str = "90D",
    created_col: str = "created_date",
    duration_col: str = "duration_days",
) -> pd.Series:
    """Trailing-window median duration per group, as-of each row's
    created_date, excluding that row itself."""
    raise NotImplementedError


def add_open_caseload_at_intake(
    df: pd.DataFrame,
    group_cols: list[str],
    created_col: str = "created_date",
    closed_col: str = "closed_date",
) -> pd.Series:
    """How many same-group requests were open at the moment this
    request was created."""
    raise NotImplementedError
