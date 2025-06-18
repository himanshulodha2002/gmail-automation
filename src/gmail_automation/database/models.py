from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String, unique=True, nullable=False)
    thread_id = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    recipients = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    received_date = Column(DateTime, default=datetime.utcnow)
    labels = Column(Text)  # Store labels as a comma-separated string
    read_status = Column(Boolean, default=False)

class RuleExecution(Base):
    __tablename__ = 'rule_executions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(Integer, ForeignKey('emails.id'), nullable=False)
    executed_at = Column(DateTime, default=datetime.utcnow)

    email = relationship("Email", back_populates="rule_executions")

Email.rule_executions = relationship("RuleExecution", order_by=RuleExecution.id, back_populates="email")