from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import List, Dict, Any

class GmailClient:
    def __init__(self, credentials: Credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def fetch_emails(self, user_id: str = 'me', max_results: int = 10) -> List[Dict[str, Any]]:
        results = self.service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        messages = results.get('messages', [])
        emails = []

        for message in messages:
            msg = self.service.users().messages().get(userId=user_id, id=message['id']).execute()
            emails.append({
                'id': msg['id'],
                'threadId': msg['threadId'],
                'subject': self._get_header(msg['payload']['headers'], 'Subject'),
                'from': self._get_header(msg['payload']['headers'], 'From'),
                'body': self._get_body(msg['payload']),
                'receivedDate': msg['internalDate'],
                'labels': msg.get('labelIds', []),
                'readStatus': 'UNREAD' not in msg.get('labelIds', [])
            })

        return emails

    def _get_header(self, headers: List[Dict[str, str]], name: str) -> str:
        for header in headers:
            if header['name'] == name:
                return header['value']
        return ''

    def _get_body(self, payload: Dict[str, Any]) -> str:
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    return part['body']['data']
        return payload['body']['data'] if 'body' in payload else ''