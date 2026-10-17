"""
Incremental client utilities for a Socrata SODA 311 dataset.

The ingestion workflow:
- retrieves records within the half-open interval (since, until]
- applies an explicit upper bound so pulls remain deterministic and replayable
- paginates through result sets that exceed the API page limit
- yields pages incrementally so downstream processing can begin before the full pull completes
- sorts records by the configured timestamp field in ascending order

Pagination continues until the API indicates that no additional rows
remain. Ordered retrieval supports reliable checkpointing and recovery
when an incremental pull is interrupted and later resumed.
"""

from __future__ import annotations


import requests
import pandas as pd
from collections.abc import Iterator
from datetime import UTC, datetime

from src.config import SOCRATA
from src.validation.validators import run_all

PAGE_SIZE = 5_000
REQUEST_TIMEOUT_SECONDS = 30


class SocrataClient:
    def __init__(self, base_url: str | None = None, app_token: str | None = None):
        self.base_url = base_url or SOCRATA.base_url
        self.app_token = app_token or SOCRATA.app_token
        self.timestamp_field = SOCRATA.timestamp_field

    def fetch_incremental(
        self, since: datetime, until: datetime | None = None
    ) -> Iterator[list[dict]]:
        """Yield pages of records with `timestamp_field` in (since, until]."""
        until = until or datetime.now(UTC)

        if since.utcoffset() is None or until.utcoffset() is None:
            raise ValueError("since and until must be timezone-aware")

        since = since.astimezone(UTC)
        until = until.astimezone(UTC)

        if since >= until:
            raise ValueError("since must be before until")

        query = f"""
            SELECT unique_key, created_date, closed_date,
                   agency, complaint_type, status,
                   {self.timestamp_field} AS source_updated_at
            WHERE {self.timestamp_field} > '{since.isoformat()}'
              AND {self.timestamp_field} <= '{until.isoformat()}'
            ORDER BY {self.timestamp_field}, unique_key
        """

        page_number = 1
        while True:
            response = requests.post(
                url=self.base_url,
                headers={"X-App-Token": self.app_token},
                json={
                    "query": query,
                    "page": {"pageSize": PAGE_SIZE, "pageNumber": page_number}
                },
                timeout=REQUEST_TIMEOUT_SECONDS
            )
            response.raise_for_status()
            records = response.json()
        
            if not records:
                break
        
            yield records
        
            if len(records) < PAGE_SIZE:
                break
        
            page_number += 1

    def fetch_all_incremental(
        self, since: datetime, until: datetime | None = None
    ) -> list[dict]:
        """Convenience wrapper: collect every page into a single list."""
        records = []
        for page in self.fetch_incremental(since, until):
            records.extend(page)
        
        return records

    def fetch_cohort(
        self, agency: str, complaint_type: str, start: datetime, end: datetime
    ) -> Iterator[list[dict]]:
        "Yield pages of request created in [start, end)"
        if start >= end:
            raise ValueError("start must be before end")

        agency_value = agency.replace("'", "''")
        complaint_value = complaint_type.replace("'", "''")

        query = f"""
                SELECT unique_key, created_date, closed_date,
                       agency, complaint_type, status
                WHERE agency = '{agency_value}'
                    AND complaint_type = '{complaint_value}'
                    AND created_date >= '{start.isoformat()}'
                    AND created_date < '{end.isoformat()}'
                ORDER BY created_date, unique_key
                """

        page_number = 1

        while True:
            response = requests.post(
                url=self.base_url,
                headers={"X-App-Token": self.app_token},
                json={
                    "query": query,
                    "page": {"pageSize": PAGE_SIZE, "pageNumber": page_number}
                },
                timeout=REQUEST_TIMEOUT_SECONDS
            )
            response.raise_for_status()
            records = response.json()

            if not records:
                break

            yield records

            if len(records) < PAGE_SIZE:
                break

            page_number += 1


if __name__ == "__main__":
    client = SocrataClient()

    records = []
    for page in client.fetch_cohort(
        agency="NYPD", complaint_type="Abandoned Vehicle", 
        start=datetime(2025, 1, 1), end=datetime(2026, 1, 1)
    ):
        records.extend(page)

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("no request returned for selected cohort")

    if "closed_date" not in df.columns:
        df["closed_date"] = pd.NaT

    for column in ("created_date", "closed_date"):
        df[column] = pd.to_datetime(df[column], errors="raise")

    df["event_indicator"] = df["closed_date"].notna().astype(int)

    run_all(df)
    print(f"validation passed for {len(df)} requests")