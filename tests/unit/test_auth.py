import pytest

from gmail_automation.auth.gmail_auth import authenticate_gmail


@pytest.fixture
def mock_credentials():
    return {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "refresh_token": "test_refresh_token"
    }

def test_authenticate_gmail_success(mocker, mock_credentials):
    # Mock the authenticate_gmail function to return a fake token
    mocker.patch(
        "gmail_automation.auth.gmail_auth.authenticate_gmail",
        return_value={"access_token": "fake_token"}
    )
    token = authenticate_gmail(mock_credentials)
    assert token is not None
    assert "access_token" in token

def test_authenticate_gmail_failure(mocker):
    # Mock to raise ValueError
    mocker.patch(
        "gmail_automation.auth.gmail_auth.authenticate_gmail",
        side_effect=ValueError("Invalid credentials")
    )
    with pytest.raises(ValueError):
        authenticate_gmail(None)

def test_authenticate_gmail_invalid_credentials(mocker):
    mocker.patch(
        "gmail_automation.auth.gmail_auth.authenticate_gmail",
        side_effect=ValueError("Invalid credentials")
    )
    invalid_credentials = {
        "client_id": "",
        "client_secret": "",
        "refresh_token": ""
    }
    with pytest.raises(ValueError):
        authenticate_gmail(invalid_credentials)