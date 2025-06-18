import pytest
from gmail_automation.auth.gmail_auth import authenticate
from gmail_automation.gmail.fetcher import fetch_emails
from gmail_automation.database.connection import get_db_session
from gmail_automation.rules.engine import evaluate_rules
from gmail_automation.rules.models import Rule
from gmail_automation.database.models import Email

@pytest.fixture
def db_session():
    session = get_db_session()
    yield session
    session.close()

@pytest.fixture
def authenticated_user():
    return authenticate()

@pytest.fixture
def sample_emails():
    return [
        {
            "message_id": "1",
            "thread_id": "1",
            "subject": "Test Email 1",
            "sender": "test1@example.com",
            "recipients": ["recipient@example.com"],
            "body": "This is a test email.",
            "received_date": "2023-01-01T12:00:00Z",
            "labels": ["INBOX"],
            "read_status": False,
        },
        {
            "message_id": "2",
            "thread_id": "2",
            "subject": "Test Email 2",
            "sender": "test2@example.com",
            "recipients": ["recipient@example.com"],
            "body": "This is another test email.",
            "received_date": "2023-01-02T12:00:00Z",
            "labels": ["INBOX"],
            "read_status": False,
        },
    ]

def test_full_workflow(authenticated_user, db_session, sample_emails):
    # Simulate fetching emails
    fetched_emails = fetch_emails(authenticated_user)
    
    # Store fetched emails in the database
    for email_data in fetched_emails:
        email = Email(**email_data)
        db_session.add(email)
    db_session.commit()

    # Define sample rules
    rules = [
        Rule(name="Test Rule", predicate="all", conditions=[
            {"field": "from", "predicate": "contains", "value": "test1@example.com"}
        ], actions=[
            {"type": "mark_as_read"}
        ])
    ]

    # Evaluate rules against fetched emails
    for rule in rules:
        evaluate_rules(rule, fetched_emails)

    # Verify that the email was marked as read
    stored_email = db_session.query(Email).filter_by(message_id="1").first()
    assert stored_email.read_status is True

    # Clean up the database
    db_session.query(Email).delete()
    db_session.commit()