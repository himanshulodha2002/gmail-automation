"""Rule engine for email processing."""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from pydantic import BaseModel, Field

from ..database.models import Email

logger = logging.getLogger(__name__)


class Condition(BaseModel):
    """Rule condition model.

    Attributes:
        field (str): The email field to check (e.g., 'from', 'subject').
        predicate (str): The condition predicate (e.g., 'contains', 'equals').
        value (str): The value to compare against.
    """

    field: str
    predicate: str
    value: str


class Action(BaseModel):
    """Rule action model.

    Attributes:
        type (str): The action type (e.g., 'mark_read', 'move_message').
        destination (str): The destination label or folder (if applicable).
    """

    type: str
    destination: str = Field(default="")


class Rule(BaseModel):
    """Email processing rule model.

    Attributes:
        name (str): Rule name.
        conditions (List[Condition]): List of conditions for the rule.
        logic (str): Logic to combine conditions ("all" for AND, "any" for OR).
        actions (List[Action]): Actions to perform if rule matches.
    """

    name: str
    conditions: List[Condition]
    logic: str = Field(default="all")  # "all" (AND) or "any" (OR)
    actions: List[Action]


class RuleEngine:
    """Engine for processing email rules."""

    def __init__(self, rules_file: str = "config/rules.json"):
        """
        Initialize the rule engine and load rules from file.

        Args:
            rules_file (str): Path to the rules JSON file.
        """
        self.rules = self._load_rules(rules_file)

    def _load_rules(self, rules_file: str) -> List[Rule]:
        """
        Load rules from JSON file.

        Args:
            rules_file (str): Path to the rules JSON file.

        Returns:
            List[Rule]: List of Rule objects.
        """
        try:
            with open(rules_file, "r") as f:
                data = json.load(f)

            rules = [Rule(**rule) for rule in data.get("rules", [])]
            logger.info(f"Loaded {len(rules)} rules from {rules_file}")
            return rules
        except Exception as e:
            logger.error(f"Error loading rules from {rules_file}: {e}")
            return []

    def evaluate_email(self, email: Email) -> List[Action]:
        """
        Evaluate email against all rules and return applicable actions.

        Args:
            email (Email): The email to evaluate.

        Returns:
            List[Action]: List of actions to perform.
        """
        applicable_actions = []

        for rule in self.rules:
            if self._evaluate_rule(email, rule):
                logger.info(f"Rule '{rule.name}' matched email {email.id}")
                applicable_actions.extend(rule.actions)

        return applicable_actions

    def _evaluate_rule(self, email: Email, rule: Rule) -> bool:
        """
        Evaluate if an email matches a rule.

        Args:
            email (Email): The email to check.
            rule (Rule): The rule to evaluate.

        Returns:
            bool: True if the rule matches, False otherwise.
        """
        condition_results = []

        for condition in rule.conditions:
            result = self._evaluate_condition(email, condition)
            condition_results.append(result)

        # Apply logic (all=AND, any=OR)
        if rule.logic == "all":
            return all(condition_results)
        elif rule.logic == "any":
            return any(condition_results)
        else:
            logger.warning(f"Unknown logic '{rule.logic}' in rule '{rule.name}'")
            return False

    def _evaluate_condition(self, email: Email, condition: Condition) -> bool:
        """
        Evaluate a single condition against an email.

        Args:
            email (Email): The email to check.
            condition (Condition): The condition to evaluate.

        Returns:
            bool: True if the condition matches, False otherwise.
        """
        field_value = self._get_field_value(email, condition.field)

        if field_value is None:
            return False

        predicate = condition.predicate.lower()
        target_value = condition.value

        try:
            if predicate == "contains":
                return target_value.lower() in str(field_value).lower()
            elif predicate == "not_contains":
                return target_value.lower() not in str(field_value).lower()
            elif predicate == "equals":
                return str(field_value).lower() == target_value.lower()
            elif predicate == "not_equals":
                return str(field_value).lower() != target_value.lower()
            elif predicate == "greater_than":
                return self._compare_dates(field_value, target_value, "greater")
            elif predicate == "less_than":
                return self._compare_dates(field_value, target_value, "less")
            else:
                logger.warning(f"Unknown predicate: {predicate}")
                return False
        except Exception as e:
            logger.error(f"Error evaluating condition: {e}")
            return False

    def _get_field_value(self, email: Email, field: str):
        """
        Get field value from email object.

        Args:
            email (Email): The email object.
            field (str): The field name.

        Returns:
            Any: The value of the field, or None if not found.
        """
        field_mapping = {
            "from": email.sender,
            "to": email.recipient,
            "subject": email.subject,
            "message": email.body,
            "received_date": email.received_at,
        }

        return field_mapping.get(field.lower())

    def _compare_dates(self, field_value, target_value: str, comparison: str) -> bool:
        """
        Compare dates for greater_than/less_than predicates.

        Args:
            field_value: The datetime value from the email.
            target_value (str): The target date expression.
            comparison (str): "greater" or "less".

        Returns:
            bool: Result of the comparison.
        """
        if not isinstance(field_value, datetime):
            return False

        # Parse relative date expressions like "7 days ago"
        target_date = self._parse_relative_date(target_value)
        if target_date is None:
            return False

        if comparison == "greater":
            return field_value > target_date
        elif comparison == "less":
            return field_value < target_date

        return False

    def _parse_relative_date(self, date_expr: str) -> Optional[datetime]:
        """
        Parse relative date expressions like '7 days ago'.

        Args:
            date_expr (str): The relative date expression.

        Returns:
            Optional[datetime]: The calculated datetime, or None if invalid.
        """
        try:
            parts = date_expr.lower().split()
            if len(parts) == 3 and parts[2] == "ago":
                amount = int(parts[0])
                unit = parts[1]

                now = datetime.utcnow()

                if unit.startswith("day"):
                    return now - timedelta(days=amount)
                elif unit.startswith("hour"):
                    return now - timedelta(hours=amount)
                elif unit.startswith("week"):
                    return now - timedelta(weeks=amount)
                elif unit.startswith("month"):
                    return now - timedelta(days=amount * 30)  # Approximate
        except Exception as e:
            logger.error(f"Error parsing relative date '{date_expr}': {e}")

        return None
