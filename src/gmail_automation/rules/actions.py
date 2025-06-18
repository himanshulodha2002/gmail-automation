from typing import List, Dict, Any

class Action:
    """Base class for actions to be taken based on rule evaluations."""
    def execute(self, email: Dict[str, Any]) -> None:
        """Execute the action on the given email."""
        raise NotImplementedError("Subclasses should implement this method.")


class MarkAsRead(Action):
    """Action to mark an email as read."""
    def execute(self, email: Dict[str, Any]) -> None:
        # Logic to mark the email as read
        email['read_status'] = True
        print(f"Email marked as read: {email['subject']}")


class MarkAsUnread(Action):
    """Action to mark an email as unread."""
    def execute(self, email: Dict[str, Any]) -> None:
        # Logic to mark the email as unread
        email['read_status'] = False
        print(f"Email marked as unread: {email['subject']}")


class MoveMessage(Action):
    """Action to move an email to a specified folder."""
    def __init__(self, destination: str):
        self.destination = destination

    def execute(self, email: Dict[str, Any]) -> None:
        # Logic to move the email to the specified folder
        email['folder'] = self.destination
        print(f"Email moved to {self.destination}: {email['subject']}")


def get_action(action_type: str, **kwargs) -> Action:
    """Factory function to get the appropriate action based on the action type."""
    if action_type == "mark_as_read":
        return MarkAsRead()
    elif action_type == "mark_as_unread":
        return MarkAsUnread()
    elif action_type == "move_message":
        return MoveMessage(kwargs.get("destination"))
    else:
        raise ValueError(f"Unknown action type: {action_type}")