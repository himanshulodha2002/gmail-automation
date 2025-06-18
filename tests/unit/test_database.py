import pytest

from gmail_automation.database.connection import Database, get_db_url
from gmail_automation.database.models import Email

def test_database_connection():
    db = Database(get_db_url())
    db.create_tables()
    assert db.engine is not None

def test_database_session():
    db = Database(get_db_url())
    with db.get_session() as session:
        assert session is not None