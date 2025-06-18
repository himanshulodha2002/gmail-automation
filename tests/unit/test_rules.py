import pytest
from gmail_automation.rules.engine import RuleEngine
from gmail_automation.rules.models import Rule

@pytest.fixture
def sample_rule():
    return Rule(
        name="Test Rule",
        predicate="all",
        conditions=[
            {"field": "from", "predicate": "contains", "value": "test@example.com"},
            {"field": "subject", "predicate": "equals", "value": "Test Subject"}
        ],
        actions=[
            {"type": "mark_as_read"},
            {"type": "move_message", "destination": "INBOX"}
        ]
    )

def test_rule_evaluation_all_conditions_met(sample_rule):
    email = {
        "from": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message.",
        "received_date": "2023-01-01T12:00:00Z",
        "read_status": False
    }
    engine = RuleEngine()
    result = engine.evaluate(sample_rule, email)
    assert result is True

def test_rule_evaluation_some_conditions_not_met(sample_rule):
    email = {
        "from": "test@example.com",
        "subject": "Different Subject",
        "message": "This is a test message.",
        "received_date": "2023-01-01T12:00:00Z",
        "read_status": False
    }
    engine = RuleEngine()
    result = engine.evaluate(sample_rule, email)
    assert result is False

def test_rule_evaluation_no_conditions_met(sample_rule):
    email = {
        "from": "other@example.com",
        "subject": "Another Subject",
        "message": "This is a test message.",
        "received_date": "2023-01-01T12:00:00Z",
        "read_status": False
    }
    engine = RuleEngine()
    result = engine.evaluate(sample_rule, email)
    assert result is False

def test_rule_evaluation_with_or_logic():
    rule = Rule(
        name="Test OR Rule",
        predicate="any",
        conditions=[
            {"field": "from", "predicate": "contains", "value": "test@example.com"},
            {"field": "subject", "predicate": "equals", "value": "Another Subject"}
        ],
        actions=[]
    )
    email = {
        "from": "other@example.com",
        "subject": "Another Subject",
        "message": "This is a test message.",
        "received_date": "2023-01-01T12:00:00Z",
        "read_status": False
    }
    engine = RuleEngine()
    result = engine.evaluate(rule, email)
    assert result is True

def test_rule_evaluation_with_invalid_rule():
    rule = None
    email = {
        "from": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message.",
        "received_date": "2023-01-01T12:00:00Z",
        "read_status": False
    }
    engine = RuleEngine()
    with pytest.raises(ValueError, match="Invalid rule provided"):
        engine.evaluate(rule, email)