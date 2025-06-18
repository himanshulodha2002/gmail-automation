import pytest
from gmail_automation.database.models import Email
from datetime import datetime

@pytest.fixture
def sample_email():
    return Email(
        id="sample_id",
        thread_id="sample_thread",
        message_id="sample_message",
        sender="sender@example.com",
        recipient="recipient@example.com",
        subject="Sample Subject",
        body="Sample Body",
        received_at=datetime.utcnow(),
        is_read=False,
        labels='["INBOX"]',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )