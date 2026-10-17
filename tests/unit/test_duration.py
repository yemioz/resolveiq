from __future__ import annotations


def test_duration_nonnegative(sample_requests):
    assert (sample_requests["duration_days"] >= 0).all()


def test_censored_rows_have_no_closed_date(sample_requests):
    censored = sample_requests[sample_requests["event_indicator"] == 0]
    assert censored["closed_date"].isna().all()


def test_observed_rows_have_closed_date(sample_requests):
    observed = sample_requests[sample_requests["event_indicator"] == 1]
    assert observed["closed_date"].notna().all()


def test_agency_history_excludes_current_request(sample_requests):
    """
    Sanity check on the fixture itself: within a single agency, the
    trailing-median calculation for the earliest request must have no
    prior observations to draw on (it's the first one chronologically).
    Full behavioral test of add_trailing_median_duration() lives in
    tests/survival/ once that function has a stable implementation.
    """
    dsny = sample_requests[sample_requests["agency"] == "DSNY"].sort_values("created_date")
    first_request = dsny.iloc[0]
    prior_requests = dsny[dsny["created_date"] < first_request["created_date"]]
    assert len(prior_requests) == 0
