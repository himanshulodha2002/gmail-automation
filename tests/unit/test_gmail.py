import pytest
from gmail_automation.gmail.client import GmailClient
from gmail_automation.auth.gmail_auth import GmailAuth

@pytest.fixture
def gmail_client():
    auth = GmailAuth()
    client = GmailClient(auth)
    return client

def test_fetch_emails(gmail_client, mocker):
    mock_response = {
        'messages': [
            {
                'id': '123',
                'threadId': '456',
                'labelIds': ['INBOX'],
                'snippet': 'Test email snippet',
                'payload': {
                    'headers': [
                        {'name': 'From', 'value': 'test@example.com'},
                        {'name': 'Subject', 'value': 'Test Subject'}
                    ],
                    'body': {
                        'data': 'Test email body'
                    }
                }
            }
        ]
    }
    
    mocker.patch('gmail_automation.gmail.client.GmailClient.fetch_emails', return_value=mock_response)
    
    emails = gmail_client.fetch_emails()
    
    assert len(emails['messages']) == 1
    assert emails['messages'][0]['payload']['headers'][0]['value'] == 'test@example.com'
    assert emails['messages'][0]['payload']['headers'][1]['value'] == 'Test Subject'

def test_handle_email_parsing(gmail_client):
    raw_email = {
        'id': '123',
        'threadId': '456',
        'labelIds': ['INBOX'],
        'snippet': 'Test email snippet',
        'payload': {
            'headers': [
                {'name': 'From', 'value': 'test@example.com'},
                {'name': 'Subject', 'value': 'Test Subject'}
            ],
            'body': {
                'data': 'Test email body'
            }
        }
    }
    
    parsed_email = gmail_client.handle_email_parsing(raw_email)
    
    assert parsed_email['from'] == 'test@example.com'
    assert parsed_email['subject'] == 'Test Subject'
    assert parsed_email['body'] == 'Test email body'