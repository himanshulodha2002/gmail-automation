import pytest

from gmail_automation.rules.engine import RuleEngine
from gmail_automation.database.models import Email

def test_rule_engine_loads_rules():
    engine = RuleEngine("config/rules.json")
    assert len(engine.rules) > 0

def test_rule_engine_evaluate_email_no_match():
    engine = RuleEngine("config/rules.json")
    email = Email(
        id="1",
        thread_id="t1",
        message_id="m1",
        sender="someone@example.com",
        recipient="me@example.com",
        subject="Hello",
        body="Test",
        received_at=None,
        is_read=False,
        labels="[]",
        created_at=None,
        updated_at=None,
    )
    actions = engine.evaluate_email(email)
    assert isinstance(actions, list)