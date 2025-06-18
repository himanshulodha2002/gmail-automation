# Gmail Automation System

This project is a Python-based email automation system that integrates with the Gmail API. It allows users to fetch emails, process them based on defined rules, and perform actions such as marking emails as read or moving them to specific folders.

## Features

- **Gmail API Integration**: Fetch emails using Google's official Python client library.
- **Rule Engine**: Process emails based on JSON-defined rules with various conditions and actions.
- **Database Storage**: Store emails and rule executions in a relational database (PostgreSQL/MySQL/SQLite3).
- **Extensible Action System**: Define actions to be taken based on rule evaluations.

## Project Structure

The project follows a modern Python project structure, which includes:

```
gmail-automation/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── uv.lock
├── noxfile.py
├── .ruff.toml
├── src/
│   └── gmail_automation/
│       ├── __init__.py
│       ├── main.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py
│       ├── auth/
│       │   ├── __init__.py
│       │   └── gmail_auth.py
│       ├── database/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── connection.py
│       │   └── migrations/
│       ├── gmail/
│       │   ├── __init__.py
│       │   ├── client.py
│       │   └── fetcher.py
│       ├── rules/
│       │   ├── __init__.py
│       │   ├── engine.py
│       │   ├── models.py
│       │   └── actions.py
│       ├── logging/
│       │   ├── __init__.py
│       │   └── config.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_auth.py
│   │   ├── test_rules.py
│   │   ├── test_database.py
│   │   └── test_gmail.py
│   ├── integration/
│   │   ├── test_full_flow.py
│   │   └── test_api_integration.py
│   └── fixtures/
│       ├── sample_emails.json
│       └── sample_rules.json
├── config/
│   ├── rules.json
│   └── logging.yaml
├── scripts/
│   ├── setup_db.py
│   └── fetch_emails.py
└── docs/
    ├── setup.md
    ├── configuration.md
    └── api.md
```

## Setup Instructions

1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd gmail-automation
   ```

2. **Install Dependencies**:
   Use the `uv` package manager to install the required dependencies:
   ```
   uv install
   ```

3. **Configure Environment Variables**:
   Set up your environment variables for Gmail API credentials. Refer to the `docs/configuration.md` for detailed instructions.

4. **Initialize the Database**:
   Run the database setup script:
   ```
   python scripts/setup_db.py
   ```

5. **Run the Application**:
   You can run the application using the command line interface:
   ```
   python src/gmail_automation/main.py
   ```

## Testing

To run the tests, use the `nox` task runner:
```
nox -s test
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.