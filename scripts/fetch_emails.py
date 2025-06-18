"""Script to fetch emails from Gmail and store in database."""

import argparse
import logging
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gmail_automation.auth.gmail_auth import GmailAuth
from gmail_automation.gmail.client import GmailClient
from gmail_automation.database.connection import get_database
from gmail_automation.database.models import Email
from gmail_automation.utils.helpers import setup_logging, load_env_file

logger = logging.getLogger(__name__)


def main():
    """Main function to fetch emails."""
    parser = argparse.ArgumentParser(description="Fetch emails from Gmail")
    parser.add_argument(
        "--query", 
        default="", 
        help="Gmail search query (default: fetch all)"
    )
    parser.add_argument(
        "--max-results", 
        type=int, 
        default=100, 
        help="Maximum number of emails to fetch"
    )
    parser.add_argument(
        "--log-level", 
        default="INFO", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Setup
    load_env_file()
    setup_logging(args.log_level)
    
    try:
        logger.info("Starting email fetch process")
        
        # Initialize components
        auth = GmailAuth()
        credentials = auth.get_credentials()
        
        if not credentials:
            logger.error("Failed to get Gmail credentials")
            return
        
        gmail_client = GmailClient(credentials)
        database = get_database()
        
        # Create tables
        database.create_tables()
        
        # Fetch messages
        messages = gmail_client.fetch_messages(args.query, args.max_results)
        
        if not messages:
            logger.info("No messages found")
            return
        
        # Process each message
        with database.get_session() as session:
            fetched_count = 0
            for message in messages:
                message_id = message['id']
                
                # Check if already exists
                existing = session.get(Email, message_id)
                if existing:
                    logger.debug(f"Email {message_id} already exists, skipping")
                    continue
                
                # Get full message details
                email = gmail_client.get_message_details(message_id)
                if email:
                    session.add(email)
                    fetched_count += 1
                    logger.debug(f"Added email: {email.subject}")
            
            logger.info(f"Successfully fetched and stored {fetched_count} new emails")
    
    except Exception as e:
        logger.error(f"Error during email fetch: {e}", exc_info=True)


if __name__ == "__main__":
    main()