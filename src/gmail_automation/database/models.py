"""Database models for email storage."""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class Email(Base):
    """Email model for storing Gmail messages."""
    
    __tablename__ = "emails"
    
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    thread_id: Mapped[str] = mapped_column(String(50), nullable=False)
    from_address: Mapped[str] = mapped_column(String(255), nullable=False)
    to_address: Mapped[Optional[str]] = mapped_column(String(255))
    subject: Mapped[Optional[str]] = mapped_column(String(500))
    message: Mapped[Optional[str]] = mapped_column(Text)
    received_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    labels: Mapped[Optional[str]] = mapped_column(String(500))  # JSON string
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<Email(id='{self.id}', subject='{self.subject}')>"
