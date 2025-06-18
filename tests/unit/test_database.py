import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gmail_automation.database.connection import get_db_session
from gmail_automation.database.models import Email, RuleExecution

@pytest.fixture(scope='module')
def test_db():
    # Setup a temporary SQLite database for testing
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create all tables
    Email.metadata.create_all(engine)
    RuleExecution.metadata.create_all(engine)

    yield session  # This will be the session used in tests

    session.close()  # Cleanup after tests

def test_email_model(test_db):
    email = Email(
        message_id='12345',
        thread_id='67890',
        subject='Test Subject',
        sender='test@example.com',
        recipients='recipient@example.com',
        body='This is a test email.',
        received_date='2023-01-01 12:00:00',
        labels='inbox',
        read_status=False
    )
    test_db.add(email)
    test_db.commit()

    assert email.id is not None
    assert email.subject == 'Test Subject'
    assert email.sender == 'test@example.com'

def test_rule_execution_model(test_db):
    rule_execution = RuleExecution(
        rule_name='Test Rule',
        executed_at='2023-01-01 12:00:00',
        email_id=1  # Assuming the email with id 1 exists
    )
    test_db.add(rule_execution)
    test_db.commit()

    assert rule_execution.id is not None
    assert rule_execution.rule_name == 'Test Rule'