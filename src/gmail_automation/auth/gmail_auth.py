from __future__ import annotations

import os
import pickle
from typing import Any, Dict, Optional

import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailAuth:
    def __init__(self, token_path: str = 'token.pickle', credentials_path: str = 'credentials.json'):
        self.token_path = token_path
        self.credentials_path = credentials_path
        self.creds: Optional[Credentials] = None
        self.load_credentials()

    def load_credentials(self) -> None:
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.creds, token)

    def get_credentials(self) -> Credentials:
        return self.creds

    def get_user_info(self) -> Dict[str, Any]:
        return {
            "token": self.creds.token,
            "expiry": self.creds.expiry,
            "refresh_token": self.creds.refresh_token,
            "client_id": self.creds.client_id,
            "client_secret": self.creds.client_secret,
        }