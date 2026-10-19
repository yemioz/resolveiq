from datetime import UTC, datetime

import pytest

from src.ingestion.postgres_loader import prepare_request


def test_prepare_request_preserves_timestamp_meaning():
    record = {
        "unique_key": "loader-test",
        "created_date": "2020-01-01T11:48:00.000",
        "source_updated_at": "2026-10-18T01:33:31.056Z",
    }

    prepared = prepare_request(record)

    assert prepared["created_date"] == datetime(2020, 1, 1, 11, 48)
    assert prepared["closed_date"] is None
    assert prepared["source_updated_at"] == datetime(2026, 10, 18, 1, 33, 31, 56000, tzinfo=UTC)


@pytest.mark.parametrize(
    "field, value",
    [
        ("created_date", "2020-01-01T11:48:00Z"),
        ("closed_date", "2020-01-02T11:48:00Z"),
        ("source_updated_at", "2026-10-18T01:33:31.056"),
    ],
)
def test_prepare_request_rejects_wrong_timezone_shape(field, value):
    record = {
        "unique_key": "loader-test",
        "created_date": "2020-01-01T11:48:00",
        "source_updated_at": "2026-10-18T01:33:31.056Z",
    }
    record[field] = value

    with pytest.raises(ValueError, match=field):
        prepare_request(record)
