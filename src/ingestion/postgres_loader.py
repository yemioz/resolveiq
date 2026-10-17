"""Persist retrieved requests to PostgreSQL."""

from sqlalchemy import create_engine, text

from src.config import DB


if __name__ == "__main__":
    engine = create_engine(DB.sqlalchemy_url)

    with engine.connect() as connection:
        database = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()

    print(f"Connected to database: {database}")
    engine.dispose()