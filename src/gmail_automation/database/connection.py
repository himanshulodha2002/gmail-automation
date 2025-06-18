from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from gmail_automation.config.settings import Settings

# Create a base class for declarative models
Base = declarative_base()

# Create a database engine
engine = create_engine(Settings.DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a scoped session for thread safety
db_session = scoped_session(SessionLocal)

def get_db():
    """Dependency that provides a database session."""
    try:
        yield db_session
    finally:
        db_session.remove()