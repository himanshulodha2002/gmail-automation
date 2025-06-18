"""Database models for email storage."""

import json
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class Email(Base):
    """Email model for storing Gmail messages."""

    __tablename__ = "emails"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    thread_id: Mapped[str] = mapped_column(String(50), nullable=False)
    message_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    sender: Mapped[str] = mapped_column(String(255), nullable=False)
    recipient: Mapped[Optional[str]] = mapped_column(String(255))
    subject: Mapped[Optional[str]] = mapped_column(String(500))
    body: Mapped[Optional[str]] = mapped_column(Text)
    received_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    labels: Mapped[Optional[str]] = mapped_column(Text)  # Storing as a JSON string

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        """
        String representation of the Email object.

        Returns:
            str: Readable representation with id and subject.
        """
        return f"<Email(id='{self.id}', subject='{self.subject}')>"

    def get_labels(self) -> List[str]:
        """
        Returns the labels from the JSON string.

        Returns:
            List[str]: List of label names or IDs.
        """
        if self.labels:
            return json.loads(self.labels)
        return []
