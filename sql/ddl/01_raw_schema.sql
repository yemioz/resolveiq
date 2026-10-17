-- Raw schema: landing zone for data as pulled from the Socrata API,
-- reshaped only enough to have typed columns.

CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.requests (
    unique_key                      TEXT PRIMARY KEY,
    created_date                    TIMESTAMPTZ NOT NULL,
    closed_date                     TIMESTAMPTZ,
    updated_at                      TIMESTAMPTZ NOT NULL,
    agency                          TEXT,
    agency_name                     TEXT,
    complaint_type                  TEXT,
    descriptor                      TEXT,
    location_type                   TEXT,
    incident_zip                    TEXT,
    borough                         TEXT,
    community_district              TEXT,
    latitude                        DOUBLE PRECISION,
    longitude                       DOUBLE PRECISION,
    open_data_channel_type          TEXT,
    status                          TEXT,
    resolution_action_updated_date  TIMESTAMPTZ,
    ingested_at                     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_raw_requests_updated_at ON raw.requests (updated_at);
CREATE INDEX IF NOT EXISTS idx_raw_requests_created_date ON raw.requests (created_date);

CREATE TABLE IF NOT EXISTS raw.agencies (
    agency      TEXT PRIMARY KEY,
    agency_name TEXT
);

CREATE TABLE IF NOT EXISTS raw.complaint_types (
    complaint_type TEXT PRIMARY KEY,
    descriptor     TEXT
);

CREATE TABLE IF NOT EXISTS raw.community_districts (
    community_district TEXT PRIMARY KEY,
    borough            TEXT
);
