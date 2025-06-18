import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.gmail_automation.database.models import Base

def setup_database(db_url: str):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    print("Database setup complete.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup_db.py <database_url>")
        sys.exit(1)

    database_url = sys.argv[1]
    setup_database(database_url)