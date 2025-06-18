import logging
import sys
import yaml
from pathlib import Path

def setup_logging(config_path: str) -> None:
    """Set up logging configuration from a YAML file."""
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)

def get_log_file_path() -> str:
    """Get the path for the log file."""
    return str(Path(__file__).resolve().parent.parent / 'logs' / 'app.log')

if __name__ == "__main__":
    log_config_path = Path(__file__).resolve().parent / 'logging.yaml'
    setup_logging(log_config_path)
    logging.info("Logging is set up.")