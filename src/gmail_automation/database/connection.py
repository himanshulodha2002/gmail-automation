"""Database connection and session management."""

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base


def get_db_url() -> str:
    """
    Get database URL from environment or use a default.

    Returns:
        str: Database connection URL.
    """
    return os.getenv("DATABASE_URL", "sqlite:///./data/gmail_automation.db")


class Database:
    """Database connection manager."""

    def __init__(self, database_url: str):
        """
        Initialize the Database connection manager.

        Args:
            database_url (str): SQLAlchemy database URL.
        """
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def create_tables(self) -> None:
        """
        Create all database tables.
        """
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get database session with automatic cleanup.

        Yields:
            Session: SQLAlchemy session object.
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# Global database instance
def get_database() -> Database:
    """
    Get database instance from environment.

    Returns:
        Database: Database connection manager instance.
    """
    database_url = os.getenv("DATABASE_URL", "sqlite:///emails.db")
    return Database(database_url)
