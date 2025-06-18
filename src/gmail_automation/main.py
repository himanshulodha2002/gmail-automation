"""Main CLI entry point for Gmail automation."""

import argparse
import sys

from .utils.helpers import load_env_file, setup_logging


def main():
    """
    Main CLI function.

    Parses command-line arguments and dispatches to the appropriate subcommand.
    """
    parser = argparse.ArgumentParser(
        description="Gmail Automation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gmail-automation fetch --query "is:unread" --max-results 50
  gmail-automation process --rules custom_rules.json --dry-run
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch emails from Gmail")
    fetch_parser.add_argument("--query", default="", help="Gmail search query")
    fetch_parser.add_argument(
        "--max-results", type=int, default=100, help="Max emails to fetch"
    )

    # Process command
    process_parser = subparsers.add_parser("process", help="Process emails with rules")
    process_parser.add_argument("--rules", default="rules.json", help="Rules file path")
    process_parser.add_argument(
        "--dry-run", action="store_true", help="Preview actions without executing"
    )

    # Global options
    parser.add_argument(
        "--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"]
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Setup
    load_env_file()
    setup_logging(args.log_level)

    if args.command == "fetch":
        from .scripts.fetch_emails import main as fetch_main

        # Override sys.argv for the fetch script
        sys.argv = [
            "fetch_emails.py",
            "--query",
            args.query,
            "--max-results",
            str(args.max_results),
            "--log-level",
            args.log_level,
        ]
        fetch_main()

    elif args.command == "process":
        from .scripts.process_rules import main as process_main

        # Override sys.argv for the process script
        sys.argv = [
            "process_rules.py",
            "--rules",
            args.rules,
            "--log-level",
            args.log_level,
        ]
        if args.dry_run:
            sys.argv.append("--dry-run")
        process_main()


if __name__ == "__main__":
    main()
