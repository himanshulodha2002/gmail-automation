"""Gmail API client for email operations."""

import base64
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

from ..database.models import Email
from ..database import get_database

logger = logging.getLogger(__name__)


class GmailClient:
    """A client to interact with the Gmail API."""

    def __init__(self, credentials_file: str, token_file: str):
        """Initializes the Gmail client."""
        self.service = self._authenticate(credentials_file, token_file)
        self._label_cache: Dict[str, str] = {}

    def _authenticate(self, credentials_file: str, token_file: str) -> Resource:
        """Authenticates the client using service account credentials."""
        from google.oauth2 import service_account

        SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

        creds = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES
        )
        return build("gmail", "v1", credentials=creds)

    def get_label_id_by_name(self, label_name: str) -> Optional[str]:
        """
        Retrieves the ID of a label by its name.
        Caches the labels to avoid repeated API calls.
        """
        if not self._label_cache:
            try:
                results = self.service.users().labels().list(userId="me").execute()
                labels = results.get("labels", [])
                self._label_cache = {label["name"]: label["id"] for label in labels}
            except HttpError as error:
                logger.error(f"An error occurred while fetching labels: {error}")
                return None

        label_id = self._label_cache.get(label_name)
        if not label_id:
            logger.warning(f"Label '{label_name}' not found.")
        return label_id

    def fetch_emails(self, query: str = "is:unread") -> List[Dict[str, Any]]:
        """Fetches emails from the user's inbox based on a query."""
        try:
            logger.info(f"Fetching emails with query: '{query}'")

            results = self.service.users().messages().list(
                userId="me",
                q=query,
                maxResults=100,
            ).execute()

            messages = results.get("messages", [])
            logger.info(f"Found {len(messages)} messages")

            return messages
        except Exception as e:
            logger.error(f"Error fetching messages: {e}")
            return []

    def get_message_details(self, message_id: str) -> Optional[Email]:
        """Get detailed message information and convert to Email model."""
        try:
            message = self.service.users().messages().get(
                userId="me",
                id=message_id,
                format="full",
            ).execute()

            return self._parse_message_to_email(message)
        except Exception as e:
            logger.error(f"Error getting message {message_id}: {e}")
            return None

    def mark_as_read(self, message_id: str) -> bool:
        """Mark message as read."""
        return self._modify_labels(message_id, remove_labels=["UNREAD"])

    def mark_as_unread(self, message_id: str) -> bool:
        """Mark message as unread."""
        return self._modify_labels(message_id, add_labels=["UNREAD"])

    def move_to_label(self, message_id: str, destination_label: str) -> bool:
        """Move message to specific label/folder."""
        # Common Gmail labels
        label_mapping = {
            "ARCHIVE": [],  # Remove INBOX
            "TRASH": ["TRASH"],
            "SPAM": ["SPAM"],
        }

        if destination_label == "ARCHIVE":
            return self._modify_labels(message_id, remove_labels=["INBOX"])
        elif destination_label in label_mapping:
            labels = label_mapping[destination_label]
            return self._modify_labels(message_id, add_labels=labels)
        else:
            logger.warning(f"Unknown destination label: {destination_label}")
            return False

    def _modify_labels(
        self,
        message_id: str,
        add_labels: Optional[List[str]] = None,
        remove_labels: Optional[List[str]] = None,
    ) -> bool:
        """Modify message labels."""
        try:
            body = {}
            if add_labels:
                body["addLabelIds"] = add_labels
            if remove_labels:
                body["removeLabelIds"] = remove_labels

            self.service.users().messages().modify(
                userId="me",
                id=message_id,
                body=body,
            ).execute()

            logger.info(f"Modified labels for message {message_id}")
            return True
        except Exception as e:
            logger.error(f"Error modifying labels for {message_id}: {e}")
            return False

    def _parse_message_to_email(self, message: Dict[str, Any]) -> Email:
        """Parse Gmail message to Email model."""
        headers = {
            h["name"].lower(): h["value"]
            for h in message.get("payload", {}).get("headers", [])
        }

        # Extract message body
        body = self._extract_message_body(message.get("payload", {}))

        # Parse date
        received_date = self._parse_date(headers.get("date", ""))

        # Check if read
        labels = message.get("labelIds", [])
        is_read = "UNREAD" not in labels

        return Email(
            id=message["id"],
            thread_id=message["threadId"],
            from_address=headers.get("from", ""),
            to_address=headers.get("to", ""),
            subject=headers.get("subject", ""),
            message=body,
            received_date=received_date,
            is_read=is_read,
            labels=json.dumps(labels),
        )

    def _extract_message_body(self, payload: Dict[str, Any]) -> str:
        """Extract text content from message payload."""
        def extract_text(part):
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8")

            if "parts" in part:
                for subpart in part["parts"]:
                    text = extract_text(subpart)
                    if text:
                        return text

            return ""

        return extract_text(payload) or ""

    def _parse_date(self, date_str: str) -> datetime:
        """Parse email date string to datetime."""
        if not date_str:
            return datetime.utcnow()

        try:
            from email.utils import parsedate_tz
            import time

            date_tuple = parsedate_tz(date_str)
            if date_tuple:
                timestamp = time.mktime(date_tuple[:9])
                return datetime.fromtimestamp(timestamp)
        except Exception as e:
            logger.warning(f"Could not parse date '{date_str}': {e}")

        return datetime.utcnow()

    def move_message(self, message_id: str, destination_label: str) -> bool:
        """Move message to a different label/folder."""
        logger.info(f"Moving message {message_id} to label {destination_label}")
        return self.move_to_label(message_id, destination_label)

    def add_label_to_message(self, message_id: str, label_id: str) -> bool:
        """Add a label to a message."""
        logger.info(f"Adding label {label_id} to message {message_id}")
        return self._modify_labels(message_id, add_labels=[label_id])


def process_rules():
    try:
        logger.info("Starting rule processing")
        
        # Initialize components
        credentials_file = os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")
        token_file = os.getenv("GMAIL_TOKEN_FILE", "token.json")
        
        gmail_client = GmailClient(credentials_file, token_file)
        database = get_database()

        # ... existing rule processing logic ...

    except Exception as e:
        logger.error(f"Error processing rules: {e}")
