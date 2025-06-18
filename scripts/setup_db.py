"""
Script to set up the database schema for the Gmail automation project.

This script creates all tables defined in the SQLAlchemy models.
Usage:
    python setup_db.py <database_url>

Arguments:
    <database_url>: SQLAlchemy-compatible database URL (e.g., sqlite:///data/gmail_automation.db)
"""

import sys

from sqlalchemy import create_engine

from gmail_automation.database.models import Base


def setup_database(db_url: str):
    """
    Create all tables in the database as defined by the SQLAlchemy models.

    Args:
        db_url (str): SQLAlchemy database URL.
    """
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    print("Database setup complete.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup_db.py <database_url>")
        sys.exit(1)

    database_url = sys.argv[1]
    setup_database(database_url)
