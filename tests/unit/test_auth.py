import pytest
from gmail_automation.auth.gmail_auth import authenticate_gmail

@pytest.fixture
def mock_credentials():
    return {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "refresh_token": "test_refresh_token"
    }

def test_authenticate_gmail_success(mock_credentials):
    token = authenticate_gmail(mock_credentials)
    assert token is not None
    assert "access_token" in token

def test_authenticate_gmail_failure():
    with pytest.raises(ValueError):
        authenticate_gmail(None)  # Simulate failure with None credentials

def test_authenticate_gmail_invalid_credentials():
    invalid_credentials = {
        "client_id": "",
        "client_secret": "",
        "refresh_token": ""
    }
    with pytest.raises(ValueError):
        authenticate_gmail(invalid_credentials)  # Simulate failure with invalid credentials