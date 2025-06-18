import pytest
from unittest.mock import MagicMock
from gmail_automation.rules.actions import ActionExecutor
from gmail_automation.rules.engine import Action
from gmail_automation.database.models import Email

@pytest.fixture
def fake_email():
    from datetime import datetime
    return Email(
        id="1",
        thread_id="t1",
        message_id="m1",
        sender="a@b.com",
        recipient="b@c.com",
        subject="Test",
        body="Body",
        received_at=datetime.utcnow(),
        is_read=False,
        labels='[]',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

def test_execute_mark_read(fake_email):
    gmail_client = MagicMock()
    gmail_client.mark_as_read.return_value = True
    database = MagicMock()
    database.get_session.return_value.__enter__.return_value.get.return_value = fake_email

    executor = ActionExecutor(gmail_client, database)
    action = Action(type="mark_read")
    assert executor.execute_actions(fake_email, [action]) is True

def test_execute_unknown_action(fake_email):
    gmail_client = MagicMock()
    database = MagicMock()
    executor = ActionExecutor(gmail_client, database)
    action = Action(type="unknown_action")
    assert executor.execute_actions(fake_email, [action]) is False