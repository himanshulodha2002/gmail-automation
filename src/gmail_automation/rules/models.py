from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    message_id = Column(String, unique=True, nullable=False)
    thread_id = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    recipients = Column(String, nullable=False)
    body = Column(String, nullable=False)
    received_date = Column(DateTime, nullable=False)
    labels = Column(JSON, nullable=True)
    read_status = Column(Boolean, default=False)

class RuleExecution(Base):
    __tablename__ = 'rule_executions'

    id = Column(Integer, primary_key=True)
    rule_name = Column(String, nullable=False)
    executed_at = Column(DateTime, nullable=False)
    email_id = Column(Integer, nullable=False)  # Foreign key to Email table
    action_taken = Column(String, nullable=False)  # Description of the action taken