import pytest

@pytest.mark.integration
def test_gmail_client_fetches_messages_with_mock():
    """
    Skipped real integration test for these reasons:
    - credentials.json is not available in CI by default.
    - Real integration would require valid Gmail API credentials and network access.
    - Avoids hitting external services during automated testing.

    TODO:
    - Add credentials.json to GitHub Actions secrets and set up the workflow to use it.
    - Once credentials are available, implement real integration tests.
    """
    pass