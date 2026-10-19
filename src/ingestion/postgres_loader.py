# Persist retrieved requests to PostgreSQL.
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import create_engine, text

from src.config import DB
from src.ingestion.socrata_client import SocrataClient


def prepare_request(record: dict) -> dict:
    closed_date = record.get("closed_date")

    prepared = {
        "unique_key": record["unique_key"],
        "created_date": datetime.fromisoformat(record["created_date"]),
        "closed_date": (datetime.fromisoformat(closed_date) if closed_date is not None else None),
        "source_updated_at": datetime.fromisoformat(record["source_updated_at"]),
        "agency": record.get("agency"),
        "complaint_type": record.get("complaint_type"),
        "status": record.get("status"),
    }

    for field in ("created_date", "closed_date"):
        value = prepared[field]
        if value is not None and value.utcoffset() is not None:
            raise ValueError(f"{field} must not contain a timezone offset")

    if prepared["source_updated_at"].utcoffset() is None:
        raise ValueError("source_updated_at must contain a timezone offset")

    return prepared


def upsert_requests(engine, records: list[dict]) -> int:
    # Persist requests and return the number inserted or updated.
    if not records:
        return 0

    statement = text(
        """
        INSERT INTO raw.requests (
            unique_key, created_date, closed_date,
            agency, complaint_type, status, updated_at
        )
        VALUES (
            :unique_key, :created_date, :closed_date,
            :agency, :complaint_type, :status, :source_updated_at
        )
        ON CONFLICT (unique_key) DO UPDATE SET
            created_date = EXCLUDED.created_date,
            closed_date = EXCLUDED.closed_date,
            agency = EXCLUDED.agency,
            complaint_type = EXCLUDED.complaint_type,
            status = EXCLUDED.status,
            updated_at = EXCLUDED.updated_at
        WHERE EXCLUDED.updated_at > raw.requests.updated_at
        """
    )

    prepared_records = [prepare_request(record) for record in records]

    with engine.begin() as connection:
        result = connection.execute(statement, prepared_records)
        affected_rows = result.rowcount

    return affected_rows


if __name__ == "__main__":
    engine = create_engine(DB.sqlalchemy_url)

    with engine.connect() as connection:
        database = connection.execute(text("SELECT current_database()")).scalar_one()

    print(f"Connected to database: {database}")

    until = datetime.now(UTC)
    since = until - timedelta(days=1)

    client = SocrataClient()
    page = next(client.fetch_incremental(since, until), [])

    print(f"records in first page: {len(page)}")
    for record in page[:3]:
        print(
            {
                field: record.get(field)
                for field in ("unique_key", "created_date", "closed_date", "source_updated_at")
            }
        )

    sample = page[:20]
    affected_rows = upsert_requests(engine, sample)
    print(f"Inserted or updated: {affected_rows} records")

    engine.dispose()
