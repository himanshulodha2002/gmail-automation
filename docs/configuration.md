# Configuration Documentation for Gmail Automation System

## Overview
This document outlines the configuration options available for the Gmail Automation System. Proper configuration is essential for the application to function correctly and efficiently.

## Configuration Files
The application uses several configuration files to manage settings:

1. **Pydantic Settings**: The main configuration is handled through Pydantic models defined in `src/gmail_automation/config/settings.py`. This file includes environment-based settings and validation.

2. **Logging Configuration**: The logging settings are defined in `config/logging.yaml`. This file specifies the logging level, format, and handlers used for structured logging.

3. **Rules Configuration**: The rules for processing emails are defined in `config/rules.json`. This JSON file contains an array of rules, each with conditions and actions.

## Environment Variables
The application can be configured using environment variables. The following variables are supported:

- `GMAIL_CLIENT_ID`: The client ID for the Gmail API.
- `GMAIL_CLIENT_SECRET`: The client secret for the Gmail API.
- `GMAIL_REFRESH_TOKEN`: The refresh token for OAuth authentication.
- `DATABASE_URL`: The connection string for the database (PostgreSQL/MySQL/SQLite).

## Logging Configuration
The logging configuration file (`logging.yaml`) supports the following options:

- **level**: The logging level (e.g., DEBUG, INFO, WARNING, ERROR).
- **format**: The format of the log messages.
- **handlers**: The handlers to use for logging (e.g., console, file).

Example of a logging configuration:
```yaml
version: 1
disable_existing_loggers: false
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    formatter: simple
    level: INFO
loggers:
  gmail_automation:
    level: DEBUG
    handlers: [console]
```

## Rules Configuration
The rules configuration file (`rules.json`) defines the rules for processing emails. Each rule includes:

- **name**: A descriptive name for the rule.
- **predicate**: The logic used to evaluate the rule (e.g., "all" or "any").
- **conditions**: An array of conditions that must be met for the rule to trigger.
- **actions**: An array of actions to take when the rule is triggered.

Example of a rules configuration:
```json
{
  "rules": [
    {
      "name": "Important emails from boss",
      "predicate": "all",
      "conditions": [
        {"field": "from", "predicate": "contains", "value": "boss@company.com"},
        {"field": "subject", "predicate": "contains", "value": "urgent"}
      ],
      "actions": [
        {"type": "mark_as_read"},
        {"type": "move_message", "destination": "IMPORTANT"}
      ]
    }
  ]
}
```

## Conclusion
Proper configuration is crucial for the Gmail Automation System to operate effectively. Ensure that all required environment variables are set and that the configuration files are correctly defined to match your operational needs.