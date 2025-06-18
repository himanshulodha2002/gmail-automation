from typing import List, Dict, Any
import json

class RuleEngine:
    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules

    def evaluate(self, email: Dict[str, Any]) -> List[Dict[str, Any]]:
        actions = []
        for rule in self.rules:
            if self._evaluate_rule(rule, email):
                actions.extend(rule.get("actions", []))
        return actions

    def _evaluate_rule(self, rule: Dict[str, Any], email: Dict[str, Any]) -> bool:
        conditions = rule.get("conditions", [])
        predicate = rule.get("predicate", "all")
        
        evaluations = [self._evaluate_condition(condition, email) for condition in conditions]
        
        if predicate == "all":
            return all(evaluations)
        elif predicate == "any":
            return any(evaluations)
        return False

    def _evaluate_condition(self, condition: Dict[str, Any], email: Dict[str, Any]) -> bool:
        field = condition.get("field")
        predicate = condition.get("predicate")
        value = condition.get("value")
        
        email_value = email.get(field, "")
        
        if predicate == "contains":
            return value in email_value
        elif predicate == "does not contain":
            return value not in email_value
        elif predicate == "equals":
            return email_value == value
        elif predicate == "does not equal":
            return email_value != value
        elif predicate in ["less than", "greater than"]:
            return self._evaluate_date_condition(predicate, email_value, value)
        
        return False

    def _evaluate_date_condition(self, predicate: str, email_date: str, value: int) -> bool:
        from datetime import datetime, timedelta
        
        email_date_obj = datetime.fromisoformat(email_date)
        comparison_date = datetime.now() - timedelta(days=value)
        
        if predicate == "less than":
            return email_date_obj < comparison_date
        elif predicate == "greater than":
            return email_date_obj > comparison_date
        
        return False

def load_rules_from_json(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data.get("rules", [])