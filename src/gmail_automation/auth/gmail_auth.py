"""Gmail OAuth2 authentication."""

import os
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


class GmailAuth:
    """Handle Gmail OAuth2 authentication."""

    def __init__(
        self,
        credentials_file: str = "credentials.json",
        token_file: str = "config/token.json",
    ):
        """
        Initialize GmailAuth.

        Args:
            credentials_file (str): Path to OAuth2 credentials file.
            token_file (str): Path to token file for storing user credentials.
        """
        self.credentials_file = credentials_file
        self.token_file = token_file

    def get_credentials(self) -> Optional[Credentials]:
        """
        Get valid Gmail API credentials.

        Returns:
            Optional[Credentials]: Google OAuth2 credentials if available.
        Raises:
            FileNotFoundError: If credentials file is missing.
        """
        creds = None

        # Load existing token
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())

        return creds
