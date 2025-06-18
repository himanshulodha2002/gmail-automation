"""Script to process stored emails with rules."""

import argparse
import logging
import os
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from gmail_automation.auth.gmail_auth import GmailAuth
from gmail_automation.database.connection import get_database
from gmail_automation.database.models import Email
from gmail_automation.gmail.client import GmailClient
from gmail_automation.rules.actions import ActionExecutor
from gmail_automation.rules.engine import RuleEngine
from gmail_automation.utils.helpers import load_env_file, setup_logging

logger = logging.getLogger(__name__)


def main():
    """Main function to process emails with rules."""
    parser = argparse.ArgumentParser(description="Process emails with rules")
    parser.add_argument(
        "--rules",
        default="config/rules.json",
        help="Rules file path (default: config/rules.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing actions",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )

    args = parser.parse_args()

    # Setup
    load_env_file()
    setup_logging(args.log_level)

    try:
        logger.info("Starting rule processing")

        # Initialize components
        auth = GmailAuth()
        credentials = auth.get_credentials()

        if not credentials:
            logger.error("Failed to get Gmail credentials")
            return

        gmail_client = GmailClient(credentials)
        database = get_database()
        rule_engine = RuleEngine(args.rules)
        action_executor = ActionExecutor(gmail_client, database)

        # Get all emails from database
        with database.get_session() as session:
            emails = session.query(Email).all()
            logger.info(f"Processing {len(emails)} emails")

            processed_count = 0
            action_count = 0

            for email in emails:
                # Evaluate email against rules
                actions = rule_engine.evaluate_email(email)

                if actions:
                    processed_count += 1
                    action_count += len(actions)

                    if args.dry_run:
                        logger.info(
                            f"[DRY RUN] Email {email.id} would execute "
                            f"{len(actions)} actions"
                        )
                        for action in actions:
                            logger.info(f"  - {action.type} {action.destination}")
                    else:
                        # Execute actions
                        success = action_executor.execute_actions(email, actions)
                        if success:
                            logger.info(f"Successfully processed email {email.id}")
                        else:
                            logger.warning(f"Some actions failed for email {email.id}")

            if args.dry_run:
                logger.info(
                    f"[DRY RUN] Would process {processed_count} emails with "
                    f"{action_count} total actions"
                )
            else:
                logger.info(
                    f"Processed {processed_count} emails with "
                    f"{action_count} total actions"
                )

    except Exception as e:
        logger.error(f"Error during rule processing: {e}", exc_info=True)


if __name__ == "__main__":
    main()
