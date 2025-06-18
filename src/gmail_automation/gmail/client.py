"""Gmail API client for email operations."""

import base64
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

from ..database.models import Email

logger = logging.getLogger(__name__)


class GmailClient:
    """A client to interact with the Gmail API."""

    def __init__(self, credentials: Credentials):
        """Initializes the Gmail client and authenticates."""
        self.service = self._authenticate(credentials)
        self._label_cache: Dict[str, str] = {}
        self._populate_label_cache()

    def _authenticate(self, credentials: Credentials) -> Resource:
        """Authenticates the client using the provided credentials."""
        return build("gmail", "v1", credentials=credentials)

    def _populate_label_cache(self):
        """Fetches all user labels and caches their names and IDs."""
        try:
            results = self.service.users().labels().list(userId="me").execute()
            labels = results.get("labels", [])
            self._label_cache = {label["name"]: label["id"] for label in labels}
            logger.info("Successfully cached user labels.")
        except HttpError as error:
            logger.error(f"An error occurred fetching labels: {error}")

    def get_label_id_by_name(self, label_name: str) -> Optional[str]:
        """Gets a label ID by its name from the cache."""
        return self._label_cache.get(label_name)

    def list_messages(self, query: str = "is:unread", max_results: int = 100) -> List[Dict[str, Any]]:
        """Lists basic message info (like IDs) from the user's inbox based on a query."""
        try:
            logger.info(f"Fetching message list with query: '{query}'")
            results = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, maxResults=max_results)
                .execute()
            )
            messages = results.get("messages", [])
            if not messages:
                logger.info("No new messages found matching the query.")
            return messages
        except HttpError as error:
            logger.error(f"An error occurred fetching the email list: {error}")
            return []

    def get_message_details(self, message_id: str) -> Optional[Email]:
        """Gets the full details for a single message and converts it to an Email object."""
        try:
            message = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )
            return self._parse_message_to_email(message)
        except HttpError as error:
            logger.error(f"An error occurred fetching details for message ID {message_id}: {error}")
            return None

    def _parse_message_to_email(self, message: Dict[str, Any]) -> Email:
        """Parses a raw Gmail API message into a structured Email object."""
        headers = message["payload"]["headers"]
        header_map = {h["name"].lower(): h["value"] for h in headers}

        received_timestamp_ms = int(message["internalDate"])
        received_at = datetime.fromtimestamp(received_timestamp_ms / 1000.0)
        
        label_ids = message.get("labelIds", [])

        return Email(
            id=message["id"],
            thread_id=message["threadId"],
            message_id=header_map.get("message-id", message["id"]),
            subject=header_map.get("subject", ""),
            sender=header_map.get("from", ""),
            recipient=header_map.get("to", ""),
            received_at=received_at,
            body=self._extract_message_body(message["payload"]),
            is_read="UNREAD" not in label_ids,
            labels=json.dumps(label_ids)
        )

    def _extract_message_body(self, payload: Dict[str, Any]) -> str:
        """Finds and decodes the text/plain part of an email's body."""
        if payload.get("body", {}).get("data"):
            data = payload["body"]["data"]
            return base64.urlsafe_b64decode(data.encode("ASCII")).decode("utf-8", "ignore")

        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    if part.get("body", {}).get("data"):
                        data = part["body"]["data"]
                        return base64.urlsafe_b64decode(data.encode("ASCII")).decode("utf-8", "ignore")
                elif "parts" in part:
                    body = self._extract_message_body(part)
                    if body:
                        return body
        return ""

    def mark_as_read(self, message_id: str) -> bool:
        """Mark a message as read by removing the 'UNREAD' label."""
        unread_label_id = self.get_label_id_by_name("UNREAD")
        if not unread_label_id:
            logger.error("Could not find the 'UNREAD' label ID.")
            return False
        return self._modify_labels(message_id, remove_labels=[unread_label_id])

    def mark_as_unread(self, message_id: str) -> bool:
        """Mark a message as unread by adding the 'UNREAD' label."""
        unread_label_id = self.get_label_id_by_name("UNREAD")
        if not unread_label_id:
            logger.error("Could not find the 'UNREAD' label ID.")
            return False
        return self._modify_labels(message_id, add_labels=[unread_label_id])

    def move_to_label(self, message_id: str, destination_label_name: str) -> bool:
        """Move a message to a new label and remove it from the inbox."""
        destination_label_id = self.get_label_id_by_name(destination_label_name)
        inbox_label_id = self.get_label_id_by_name("INBOX")

        if not destination_label_id:
            logger.error(f"Destination label '{destination_label_name}' not found.")
            return False

        add_labels = [destination_label_id]
        remove_labels = [inbox_label_id] if inbox_label_id else []

        return self._modify_labels(message_id, add_labels=add_labels, remove_labels=remove_labels)

    def _modify_labels(
        self,
        message_id: str,
        add_labels: Optional[List[str]] = None,
        remove_labels: Optional[List[str]] = None,
    ) -> bool:
        """A helper function to add or remove labels from a message."""
        body = {
            "addLabelIds": add_labels or [],
            "removeLabelIds": remove_labels or [],
        }
        try:
            self.service.users().messages().modify(
                userId="me", id=message_id, body=body
            ).execute()
            logger.info(f"Successfully modified labels for message {message_id}.")
            return True
        except HttpError as error:
            logger.error(f"Failed to modify labels for message {message_id}: {error}")
            return False
