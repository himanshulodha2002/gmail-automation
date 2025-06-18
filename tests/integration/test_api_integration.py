import pytest

from gmail_automation.auth.gmail_auth import authenticate
from gmail_automation.database.connection import get_db_session
from gmail_automation.database.models import Email
from gmail_automation.rules.engine import RuleEngine


@pytest.fixture
def gmail_client():
    """Fixture to create a Gmail client instance."""
    client = authenticate()
    yield client
    client.close()

@pytest.fixture
def db_session():
    """Fixture to create a database session."""
    session = get_db_session()
    yield session
    session.close()

@pytest.fixture
def rule_engine():
    """Fixture to create a Rule Engine instance."""
    engine = RuleEngine()
    yield engine

def test_fetch_emails(gmail_client, db_session):
    """Test fetching emails from the Gmail API."""
    emails = gmail_client.fetch_emails()
    assert emails is not None
    assert isinstance(emails, list)

    # Optionally, you can add code to store emails in the database
    for email in emails:
        db_session.add(email)
    db_session.commit()

def test_rule_engine_processing(rule_engine, db_session):
    """Test the rule engine processing."""
    # Load sample rules from a fixture or define them here
    sample_rules = [
        {
            "name": "Test Rule",
            "logic": "all",
            "conditions": [
                {"field": "from", "predicate": "contains", "value": "test@example.com"}
            ],
            "actions": [
                {"type": "mark_as_read"}
            ]
        }
    ]
    rule_engine.load_rules(sample_rules)
    emails = db_session.query(Email).all()
    for email in emails:
        rule_engine.evaluate(email)
    assert all(email.read_status for email in emails if email.sender == "test@example.com")

def test_api_integration(gmail_client):
    """Test the integration with the Gmail API."""
    response = gmail_client.get_user_profile()
    assert response is not None
    assert 'emailAddress' in response
    # Optionally, check for a valid email address format
    assert '@' in response['emailAddress']