"""Script to fetch emails from Gmail and store in database."""

import argparse
import logging
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gmail_automation.database.connection import Database, get_db_url
from gmail_automation.database.models import Email
from gmail_automation.gmail.client import GmailClient
from gmail_automation.auth.gmail_auth import GmailAuth

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    """Main function to fetch emails."""
    parser = argparse.ArgumentParser(description="Fetch emails from Gmail.")
    parser.add_argument("--query", type=str, default="is:unread", help="Gmail search query.")
    parser.add_argument("--max-results", type=int, default=100, help="Maximum number of emails to fetch.")
    args = parser.parse_args()

    logger.info("Starting email fetch process")
    try:
        auth = GmailAuth()
        credentials = auth.get_credentials()
        if not credentials:
            logger.error("Failed to get credentials.")
            sys.exit(1)

        gmail_client = GmailClient(credentials)
        database = Database(get_db_url())

        # Create tables if they don't exist
        database.create_tables()

        # 1. Get the list of message IDs
        message_list = gmail_client.list_messages(query=args.query, max_results=args.max_results)

        if not message_list:
            logger.info("No new messages to process.")
            return

        logger.info(f"Found {len(message_list)} messages to process.")

        saved_count = 0
        with database.get_session() as session:
            for message_info in message_list:
                message_id = message_info["id"]

                # Check if email already exists in the database
                exists = session.query(Email).filter_by(id=message_id).first()
                if exists:
                    logger.debug(f"Skipping already existing email with ID: {message_id}")
                    continue

                # 2. Get the full details for each new message
                email_details = gmail_client.get_message_details(message_id)

                if email_details:
                    session.add(email_details)
                    saved_count += 1

            if saved_count > 0:
                logger.info(f"Successfully fetched and stored {saved_count} new emails.")
            else:
                logger.info("No new emails were stored (all were duplicates).")

    except Exception as e:
        logger.error(f"An error occurred during the email fetch process: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()