import pytest

@pytest.mark.integration
def test_end_to_end_email_processing_with_mock():
    """
    Skipped real integration test for these reasons:
    - credentials.json is not available in CI by default.
    - Real integration would require valid Gmail API credentials, a test database, and network access.
    - Avoids hitting external services and database during automated testing.

    TODO:
    - Add credentials.json to GitHub Actions secrets and set up the workflow to use it.
    - Once credentials are available, implement real end-to-end integration tests.
    """
    pass
