from gmail_automation.config.settings import Settings
from gmail_automation.auth.gmail_auth import authenticate
from gmail_automation.database.connection import get_db_session
from gmail_automation.gmail.fetcher import fetch_emails
from gmail_automation.rules.engine import RuleEngine
import argparse
import logging

def main():
    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Load configuration
    settings = Settings()

    # Authenticate with Gmail API
    logger.info("Authenticating with Gmail API...")
    service = authenticate(settings)

    # Create a database session
    logger.info("Connecting to the database...")
    session = get_db_session(settings)

    # Fetch emails
    logger.info("Fetching emails...")
    emails = fetch_emails(service)

    # Process rules
    logger.info("Processing rules...")
    rule_engine = RuleEngine(session)
    rule_engine.process(emails)

    logger.info("Email processing completed.")

if __name__ == "__main__":
    main()