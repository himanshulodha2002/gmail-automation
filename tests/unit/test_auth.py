import pytest

from gmail_automation.auth.gmail_auth import GmailAuth

def test_gmail_auth_init():
    auth = GmailAuth()
    assert auth.credentials_file.endswith("credentials.json")
    assert auth.token_file.endswith("token.json")