from typing import List, Dict, Any
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import logging

class GmailFetcher:
    def __init__(self, creds_file: str, scopes: List[str]):
        self.creds_file = creds_file
        self.scopes = scopes
        self.service = self.authenticate()

    def authenticate(self) -> Any:
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.creds_file, self.scopes)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)

    def fetch_emails(self, user_id: str = 'me', query: str = '', max_results: int = 10) -> List[Dict[str, Any]]:
        try:
            results = self.service.users().messages().list(userId=user_id, q=query, maxResults=max_results).execute()
            messages = results.get('messages', [])
            emails = []
            for message in messages:
                msg = self.service.users().messages().get(userId=user_id, id=message['id']).execute()
                emails.append({
                    'id': msg['id'],
                    'threadId': msg['threadId'],
                    'subject': self.get_header(msg['payload']['headers'], 'Subject'),
                    'from': self.get_header(msg['payload']['headers'], 'From'),
                    'body': self.get_body(msg['payload']),
                    'received_date': msg['internalDate'],
                    'labels': msg.get('labelIds', []),
                    'read_status': 'UNREAD' not in msg.get('labelIds', [])
                })
            return emails
        except Exception as e:
            logging.error(f"An error occurred while fetching emails: {e}")
            return []

    def get_header(self, headers: List[Dict[str, str]], name: str) -> str:
        for header in headers:
            if header['name'] == name:
                return header['value']
        return ''

    def get_body(self, payload: Dict[str, Any]) -> str:
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    return part['body']['data']
        return payload['body']['data'] if 'body' in payload else ''
