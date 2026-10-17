-- Staging schema: cleaned and deduplicated records, one row per
-- unique_key, still close to source grain. Business/dimensional

CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.stg_requests (
    unique_key                      TEXT PRIMARY KEY,
    created_date                    TIMESTAMPTZ NOT NULL,
    closed_date                     TIMESTAMPTZ,
    agency                          TEXT NOT NULL,
    complaint_type                  TEXT NOT NULL,
    borough                         TEXT,
    community_district              TEXT,
    incident_zip                    TEXT,
    latitude                        DOUBLE PRECISION,
    longitude                       DOUBLE PRECISION,
    open_data_channel_type          TEXT,
    status                          TEXT NOT NULL,
    -- derived at staging time, not analytics time, so downstream
    -- consumers don't each reimplement the censoring rule differently
    is_closed                       BOOLEAN NOT NULL,
    duration_days                   NUMERIC,   -- vs. closed_date if closed, vs. snapshot if open
    snapshot_time                   TIMESTAMPTZ NOT NULL,
    loaded_at                       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS staging.stg_agency_daily_load (
    agency          TEXT NOT NULL,
    activity_date   DATE NOT NULL,
    requests_opened INTEGER NOT NULL DEFAULT 0,
    requests_closed INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (agency, activity_date)
);

CREATE TABLE IF NOT EXISTS staging.stg_complaint_type_daily_load (
    complaint_type   TEXT NOT NULL,
    activity_date    DATE NOT NULL,
    requests_opened  INTEGER NOT NULL DEFAULT 0,
    requests_closed  INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (complaint_type, activity_date)
);
