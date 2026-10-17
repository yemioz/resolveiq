from __future__ import annotations

import pytest
import pandas as pd

from src.validation.validators import (
    ValidationError,
    validate_business_rules,
    validate_censoring_consistency,
    validate_grain,
    validate_schema,
    run_all
)


def test_requests_are_unique(sample_requests):
    validate_grain(sample_requests)  # should not raise


def test_duplicate_unique_key_raises(sample_requests):
    duped = sample_requests.copy()
    duped = duped._append(duped.iloc[0])  # introduce a duplicate
    with pytest.raises(ValidationError):
        validate_grain(duped)


def test_schema_passes_on_valid_fixture(sample_requests):
    validate_schema(sample_requests)  # should not raise


def test_created_after_closed_raises(sample_requests):
    bad = sample_requests.copy()
    bad.loc[0, "created_date"] = bad.loc[0, "closed_date"] + __import__("pandas").Timedelta(days=1)
    with pytest.raises(ValidationError):
        validate_business_rules(bad)


def test_censoring_consistency_passes_on_valid_fixture(sample_requests):
    validate_censoring_consistency(sample_requests)  # should not raise


def test_censored_row_with_closed_date_raises(sample_requests):
    bad = sample_requests.copy()
    open_idx = bad[bad["event_indicator"] == 0].index[0]
    bad.loc[open_idx, "closed_date"] = bad.loc[open_idx, "created_date"]
    with pytest.raises(ValidationError):
        validate_censoring_consistency(bad)


def test_observed_event_without_closed_date_raises(sample_requests):
    bad = sample_requests.copy()
    bad.loc[0, "event_indicator"] = 1
    bad.loc[0, "closed_date"] = pd.NaT

    with pytest.raises(ValidationError):
        validate_censoring_consistency(bad)


@pytest.mark.parametrize("invalid_event", [2, -1, None])
def test_invalid_event_indicator_raises(sample_requests, invalid_event):
    bad = sample_requests.copy()
    bad["event_indicator"] = bad["event_indicator"].astype("object")
    bad.loc[0, "event_indicator"] = invalid_event

    with pytest.raises(ValidationError):
        validate_censoring_consistency(bad)


def test_run_all_passes_on_valid_fixture(sample_requests):
    run_all(sample_requests)
