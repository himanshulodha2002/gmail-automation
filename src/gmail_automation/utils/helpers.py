"""Utility functions and helpers."""

import logging
import os
from typing import Optional


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    log_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def load_env_file(env_file: str = ".env") -> None:
    """Load environment variables from file."""
    if os.path.exists(env_file):
        from dotenv import load_dotenv

        load_dotenv(env_file)


def get_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable with optional default."""
    return os.getenv(name, default)
