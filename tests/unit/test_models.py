from gmail_automation.database.models import Email
from datetime import datetime

def test_email_get_labels():
    email = Email(
        id="1",
        thread_id="t1",
        message_id="m1",
        sender="a@b.com",
        recipient="b@c.com",
        subject="Test",
        body="Body",
        received_at=datetime.utcnow(),
        is_read=False,
        labels='["INBOX", "IMPORTANT"]',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    assert email.get_labels() == ["INBOX", "IMPORTANT"]

def test_email_repr():
    email = Email(
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
    assert "<Email(id='1', subject='Test')" in repr(email)