from __future__ import annotations

import pytest

from src.survival.kaplan_meier import (
    compare_groups_logrank,
    fit_km_by_group,
    survival_probability_at,
)


def test_km_curve_monotonic_nonincreasing(sample_requests):
    fitters = fit_km_by_group(sample_requests, group_col="agency")
    for kmf in fitters.values():
        surv = kmf.survival_function_.iloc[:, 0]
        assert (surv.diff().dropna() <= 1e-9).all(), "KM survival curve must be non-increasing"


def test_survival_probability_between_zero_and_one(sample_requests):
    fitters = fit_km_by_group(sample_requests, group_col="agency")
    for kmf in fitters.values():
        max_time = kmf.durations.max()
        prob = survival_probability_at(kmf, time_horizon=max_time / 2)
        assert 0.0 <= prob <= 1.0


def test_logrank_returns_p_value(sample_requests):
    result = compare_groups_logrank(sample_requests, group_col="agency")
    assert 0.0 <= result["p_value"] <= 1.0


@pytest.mark.skip(reason="Requires a fitted CoxPHFitter with enough data to converge -- "
                          "enable once fit_cox_model() is exercised against real feature data.")
def test_ph_assumption_check_runs():
    ...


@pytest.mark.skip(reason="No trained model artifact yet -- placeholder for the leakage "
                          "test described in the project spec.")
def test_no_future_features():
    ...
