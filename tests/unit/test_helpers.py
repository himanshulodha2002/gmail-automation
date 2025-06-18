import os
import logging
from gmail_automation.utils import helpers

def test_setup_logging_sets_level(monkeypatch):
    # Reset logging config for the test
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    helpers.setup_logging("DEBUG")
    assert logging.getLogger().getEffectiveLevel() == logging.DEBUG

def test_get_env_var_returns_value(monkeypatch):
    monkeypatch.setenv("FOO", "bar")
    assert helpers.get_env_var("FOO") == "bar"

def test_get_env_var_returns_default():
    assert helpers.get_env_var("NOT_SET", "default") == "default"