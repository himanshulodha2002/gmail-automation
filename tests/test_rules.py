"""Unit tests for rule engine."""

import json
import tempfile
from datetime import datetime, timedelta

import pytest

from gmail_automation.rules.engine import RuleEngine, Rule, Condition, Action
from gmail_automation.database.models import Email


class TestRuleEngine:
    """Test cases for RuleEngine."""
    
    def test_load_rules_from_file(self):
        """Test loading rules from JSON file."""
        rules_data = {
            "rules": [
                {
                    "name": "Test Rule",
                    "conditions": [
                        {
                            "field": "from",
                            "predicate": "contains",
                            "value": "test"
                        }
                    ],
                    "logic": "all",
                    "actions": [
                        {
                            "type": "mark_read"
                        }
                    ]
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(rules_data, f)
            rules_file = f.name
        
        engine = RuleEngine(rules_file)
        assert len(engine.rules) == 1
        assert engine.rules[0].name == "Test Rule"
    
    def test_contains_predicate(self):
        """Test contains predicate evaluation."""
        email = Email(
            id="test1",
            thread_id="thread1",
            from_address="noreply@example.com",
            subject="Test Subject",
            message="Test message",
            received_date=datetime.utcnow()
        )
        
        condition = Condition(field="from", predicate="contains", value="noreply")
        
        # Create a simple rule engine
        engine = RuleEngine("nonexistent.json")  # Won't load any rules
        
        result = engine._evaluate_condition(email, condition)
        assert result is True
    
    def test_not_contains_predicate(self):
        """Test not_contains predicate evaluation."""
        email = Email(
            id="test1",
            thread_id="thread1",
            from_address="user@example.com",
            subject="Test Subject",
            message="Test message",
            received_date=datetime.utcnow()
        )
        
        condition = Condition(field="from", predicate="not_contains", value="noreply")
        
        engine = RuleEngine("nonexistent.json")
        result = engine._evaluate_condition(email, condition)
        assert result is True
    
    def test_equals_predicate(self):
        """Test equals predicate evaluation."""
        email = Email(
            id="test1",
            thread_id="thread1",
            from_address="boss@company.com",
            subject="Test Subject",
            message="Test message",
            received_date=datetime.utcnow()
        )
        
        condition = Condition(field="from", predicate="equals", value="boss@company.com")
        
        engine = RuleEngine("nonexistent.json")
        result = engine._evaluate_condition(email, condition)
        assert result is True
    
    def test_date_comparison(self):
        """Test date comparison predicates."""
        # Email from 10 days ago
        old_date = datetime.utcnow() - timedelta(days=10)
        email = Email(
            id="test1",
            thread_id="thread1",
            from_address="test@example.com",
            subject="Old Email",
            message="Test message",
            received_date=old_date
        )
        
        condition = Condition(field="received_date", predicate="less_than", value="7 days ago")
        
        engine = RuleEngine("nonexistent.json")
        result = engine._evaluate_condition(email, condition)
        assert result is True
    
    def test_rule_logic_all(self):
        """Test rule evaluation with 'all' logic (AND)."""
        email = Email(
            id="test1",
            thread_id="thread1",
            from_address="noreply@example.com",
            subject="Newsletter",
            message="Test message",
            received_date=datetime.utcnow()
        )
        
        rule = Rule(
            name="Test Rule",
            conditions=[
                Condition(field="from", predicate="contains", value="noreply"),
                Condition(field="subject", predicate="contains", value="Newsletter")
            ],
            logic="all",
            actions=[Action(type="mark_read")]
        )
        
        engine = RuleEngine("nonexistent.json")
        result = engine._evaluate_rule(email, rule)
        assert result is True
    
    def test_rule_logic_any(self):
        """Test rule evaluation with 'any' logic (OR)."""
        email = Email(
            id="test1",
            thread_id="thread1",
            from_address="user@example.com",
            subject="Newsletter",
            message="Test message",
            received_date=datetime.utcnow()
        )
        
        rule = Rule(
            name="Test Rule",
            conditions=[
                Condition(field="from", predicate="contains", value="noreply"),
                Condition(field="subject", predicate="contains", value="Newsletter")
            ],
            logic="any",
            actions=[Action(type="mark_read")]
        )
        
        engine = RuleEngine("nonexistent.json")
        result = engine._evaluate_rule(email, rule)
        assert result is True  # Should match because subject contains "Newsletter"


if __name__ == "__main__":
    pytest.main([__file__])
