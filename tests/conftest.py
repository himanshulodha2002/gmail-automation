import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.gmail_automation.database.connection import get_db_session

@pytest.fixture(scope='session')
def db_engine():
    # Create a new database engine for testing
    engine = create_engine('sqlite:///:memory:', echo=True)
    yield engine
    engine.dispose()

@pytest.fixture(scope='function')
def db_session(db_engine):
    # Create a new session for each test
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=db_engine)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def mock_gmail_api(mocker):
    # Mock the Gmail API client for testing
    mock_client = mocker.patch('src.gmail_automation.gmail.client.GmailClient')
    return mock_client

@pytest.fixture(scope='function')
def sample_email_data():
    return {
        "id": "12345",
        "message_id": "abcde",
        "thread_id": "67890",
        "subject": "Test Email",
        "sender": "test@example.com",
        "recipients": ["recipient@example.com"],
        "body": "This is a test email.",
        "received_date": "2023-10-01T12:00:00Z",
        "labels": ["INBOX"],
        "read_status": False
    }

@pytest.fixture(scope='function')
def sample_rule_data():
    return {
        "name": "Test Rule",
        "predicate": "all",
        "conditions": [
            {"field": "from", "predicate": "contains", "value": "test@example.com"},
            {"field": "subject", "predicate": "contains", "value": "Test"}
        ],
        "actions": [
            {"type": "mark_as_read"},
            {"type": "move_message", "destination": "IMPORTANT"}
        ]
    }