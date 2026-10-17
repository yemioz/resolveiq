"""
Central configuration for ResolvIQ.

Every other module reads settings from here instead of calling
os.environ directly, so there's one place that knows how the app
is configured and one place to change it (e.g. for tests).
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()  # no-op if .env doesn't exist (e.g. in CI, where env vars are injected directly)


@dataclass(frozen=True)
class DatabaseConfig:
    host: str = os.getenv("RESOLVIQ_DB_HOST", "localhost")
    port: int = int(os.getenv("RESOLVIQ_DB_PORT", "5432"))
    name: str = os.getenv("RESOLVIQ_DB_NAME", "resolviq")
    user: str = os.getenv("RESOLVIQ_DB_USER", "resolviq")
    password: str = os.getenv("RESOLVIQ_DB_PASSWORD", "")

    @property
    def sqlalchemy_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


@dataclass(frozen=True)
class SocrataConfig:
    base_url: str = os.getenv(
        "SOCRATA_BASE_URL", "https://data.cityofnewyork.us/api/v3/views/erm2-nwe9/query.json"
    )
    app_token: str = os.getenv("SOCRATA_APP_TOKEN", "")
    timestamp_field: str = os.getenv("SOCRATA_TIMESTAMP_FIELD", ":updated_at")


@dataclass(frozen=True)
class ModelConfig:
    version: str = os.getenv("MODEL_VERSION", "0.1.0")
    sla_default_days: int = int(os.getenv("SLA_DEFAULT_DAYS", "14"))


DB = DatabaseConfig()
SOCRATA = SocrataConfig()
MODEL = ModelConfig()
