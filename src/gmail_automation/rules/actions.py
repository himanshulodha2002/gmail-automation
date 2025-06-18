"""Action execution for email operations."""

import logging
from typing import List

from ..database.connection import Database
from ..database.models import Email
from ..gmail.client import GmailClient
from .engine import Action

logger = logging.getLogger(__name__)


class ActionExecutor:
    """Execute actions on emails."""

    def __init__(self, gmail_client: GmailClient, database: Database):
        """
        Initialize the ActionExecutor.

        Args:
            gmail_client (GmailClient): The Gmail API client.
            database (Database): The database connection manager.
        """
        self.gmail_client = gmail_client
        self.database = database

    def execute_actions(self, email: Email, actions: List[Action]) -> bool:
        """
        Execute a list of actions on an email.

        Args:
            email (Email): The email to act on.
            actions (List[Action]): List of actions to execute.

        Returns:
            bool: True if all actions succeeded, False otherwise.
        """
        success = True

        for action in actions:
            try:
                result = self._execute_single_action(email, action)
                if not result:
                    success = False
                    logger.error(
                        f"Failed to execute action {action.type} on email {email.id}"
                    )
            except Exception as e:
                logger.error(f"Error executing action {action.type}: {e}")
                success = False

        return success

    def _execute_single_action(self, email: Email, action: Action) -> bool:
        """
        Execute a single action on an email.

        Args:
            email (Email): The email to act on.
            action (Action): The action to execute.

        Returns:
            bool: True if the action succeeded, False otherwise.
        """
        action_type = action.type.lower()

        if action_type == "mark_read":
            return self._mark_as_read(email)
        elif action_type == "mark_unread":
            return self._mark_as_unread(email)
        elif action_type == "move_message":
            return self._move_message(email, action.destination)
        else:
            logger.warning(f"Unknown action type: {action_type}")
            return False

    def _mark_as_read(self, email: Email) -> bool:
        """
        Mark email as read.

        Args:
            email (Email): The email to mark as read.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self.gmail_client.mark_as_read(email.id):
            # Update database
            with self.database.get_session() as session:
                db_email = session.get(Email, email.id)
                if db_email:
                    db_email.is_read = True
                    logger.info(f"Marked email {email.id} as read")
            return True
        return False

    def _mark_as_unread(self, email: Email) -> bool:
        """
        Mark email as unread.

        Args:
            email (Email): The email to mark as unread.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self.gmail_client.mark_as_unread(email.id):
            # Update database
            with self.database.get_session() as session:
                db_email = session.get(Email, email.id)
                if db_email:
                    db_email.is_read = False
                    logger.info(f"Marked email {email.id} as unread")
            return True
        return False

    def _move_message(self, email: Email, destination: str) -> bool:
        """
        Move email to specified destination.

        Args:
            email (Email): The email to move.
            destination (str): The destination label or folder.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self.gmail_client.move_to_label(email.id, destination):
            logger.info(f"Moved email {email.id} to {destination}")
            return True
        return False
