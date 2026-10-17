from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import pytest


@pytest.fixture
def snapshot_time() -> datetime:
    return datetime(2026, 6, 1, 0, 0, 0)  # noqa: DTZ001 -- naive is fine for this fixture


@pytest.fixture
def sample_requests(snapshot_time) -> pd.DataFrame:
    """
    A small synthetic fixture with a mix of closed and still-open
    (censored) requests, spanning two agencies -- enough to exercise
    validation, feature, and survival-model code paths without a
    real database or a live API call.
    """
    created = [snapshot_time - timedelta(days=d) for d in [30, 25, 20, 15, 10, 5]]
    closed = [
        snapshot_time - timedelta(days=25),
        snapshot_time - timedelta(days=15),
        None,  # still open
        snapshot_time - timedelta(days=5),
        None,  # still open
        None,  # still open
    ]

    df = pd.DataFrame(
        {
            "unique_key": [f"REQ{i}" for i in range(6)],
            "created_date": created,
            "closed_date": closed,
            "agency": ["DSNY", "DSNY", "DSNY", "HPD", "HPD", "HPD"],
            "complaint_type": [
                "Missed Collection",
                "Missed Collection",
                "Illegal Dumping",
                "Heat/Hot Water",
                "Heat/Hot Water",
                "Plumbing",
            ],
            "status": ["Closed", "Closed", "Open", "Closed", "Open", "Open"],
        }
    )
    df["event_indicator"] = df["closed_date"].notna().astype(int)
    df["duration_days"] = (
        df["closed_date"].fillna(snapshot_time) - df["created_date"]
    ).dt.total_seconds() / 86400
    return df
