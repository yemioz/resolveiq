-- Analytics schema: dimensional model + feature tables + model outputs.
-- This is what the modeling code and Power BI both read from.

CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.dim_agency (
    agency_id     SERIAL PRIMARY KEY,
    agency        TEXT UNIQUE NOT NULL,
    agency_name   TEXT
);

CREATE TABLE IF NOT EXISTS analytics.dim_complaint_type (
    complaint_id    SERIAL PRIMARY KEY,
    complaint_type  TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS analytics.dim_geography (
    geography_id         SERIAL PRIMARY KEY,
    borough              TEXT,
    community_district   TEXT,
    UNIQUE (borough, community_district)
);

CREATE TABLE IF NOT EXISTS analytics.dim_date (
    date_id      DATE PRIMARY KEY,
    year         INTEGER NOT NULL,
    month        INTEGER NOT NULL,
    day          INTEGER NOT NULL,
    day_of_week  TEXT NOT NULL,
    is_weekend   BOOLEAN NOT NULL
);

-- Grain: 1 row = 1 service request.
CREATE TABLE IF NOT EXISTS analytics.fact_requests (
    request_id            TEXT PRIMARY KEY REFERENCES staging.stg_requests (unique_key),
    agency_id             INTEGER NOT NULL REFERENCES analytics.dim_agency (agency_id),
    complaint_id          INTEGER NOT NULL REFERENCES analytics.dim_complaint_type (complaint_id),
    geography_id          INTEGER REFERENCES analytics.dim_geography (geography_id),
    created_date           TIMESTAMPTZ NOT NULL,
    closed_date            TIMESTAMPTZ,
    duration_days           NUMERIC NOT NULL,
    event_indicator          SMALLINT NOT NULL CHECK (event_indicator IN (0, 1)), -- 1=closed, 0=censored
    open_data_channel_type  TEXT
);

-- Grain: 1 row = 1 agency-date combination.
CREATE TABLE IF NOT EXISTS analytics.agency_daily_backlog (
    agency_id            INTEGER NOT NULL REFERENCES analytics.dim_agency (agency_id),
    activity_date        DATE NOT NULL,
    open_caseload        INTEGER NOT NULL,
    avg_open_case_age    NUMERIC,
    closed_today         INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (agency_id, activity_date)
);

-- Grain: 1 row = 1 service request, with point-in-time features only.
CREATE TABLE IF NOT EXISTS analytics.survival_features (
    request_id                        TEXT PRIMARY KEY REFERENCES analytics.fact_requests (request_id),
    duration_days                     NUMERIC NOT NULL,
    event_indicator                   SMALLINT NOT NULL CHECK (event_indicator IN (0, 1)),
    agency_id                         INTEGER NOT NULL,
    complaint_id                      INTEGER NOT NULL,
    geography_id                      INTEGER,
    open_data_channel_type            TEXT,
    hour_of_day                       SMALLINT,
    day_of_week                       TEXT,
    month                             SMALLINT,
    agency_trailing_90d_median_days   NUMERIC,  -- as-of created_date, excludes current row
    complaint_trailing_90d_median_days NUMERIC, -- as-of created_date, excludes current row
    agency_open_caseload_at_intake    INTEGER,
    feature_computed_at               TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Grain: 1 row = 1 prediction for 1 request at 1 point in time.
CREATE TABLE IF NOT EXISTS analytics.model_predictions (
    prediction_id                     BIGSERIAL PRIMARY KEY,
    request_id                        TEXT NOT NULL REFERENCES analytics.fact_requests (request_id),
    prediction_timestamp              TIMESTAMPTZ NOT NULL DEFAULT now(),
    model_version                     TEXT NOT NULL,
    survival_probability_at_sla       NUMERIC,
    predicted_median_resolution_days  NUMERIC,
    extreme_delay_probability         NUMERIC,
    risk_band                         TEXT,
    actual_outcome                    SMALLINT  -- populated once the case closes
);

CREATE INDEX IF NOT EXISTS idx_model_predictions_request
    ON analytics.model_predictions (request_id);
