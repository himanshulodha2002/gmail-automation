def parse_json_file(file_path: str) -> dict:
    """Parse a JSON file and return its contents as a dictionary."""
    import json
    from pathlib import Path

    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"{file_path} does not exist.")

    with file_path.open('r', encoding='utf-8') as file:
        return json.load(file)

def format_email_body(body: str) -> str:
    """Format the email body for better readability."""
    return body.strip().replace('\n', ' ').replace('\r', '')

def is_valid_email(email: str) -> bool:
    """Check if the provided string is a valid email format."""
    import re
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def get_current_timestamp() -> str:
    """Return the current timestamp in ISO format."""
    from datetime import datetime
    return datetime.now().isoformat()