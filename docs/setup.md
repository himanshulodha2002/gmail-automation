# Setup Instructions for Gmail Automation Project

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.8 or higher
- PostgreSQL, MySQL, or SQLite3 (depending on your choice of database)
- pip (Python package installer)
- uv (modern Python package manager)

## Installation Steps

1. **Clone the Repository**

   Clone the project repository from GitHub:

   ```
   git clone https://github.com/yourusername/gmail-automation.git
   cd gmail-automation
   ```

2. **Set Up Python Environment**

   Create a virtual environment and activate it:

   ```
   uv create .python-version
   uv install
   ```

3. **Install Dependencies**

   Install the required dependencies using uv:

   ```
   uv install
   ```

   This will install all the necessary packages as specified in `pyproject.toml`.

4. **Configure Database**

   Update the database configuration in `src/gmail_automation/config/settings.py` to match your database setup. Ensure that the database server is running and accessible.

5. **Run Database Migrations**

   Initialize the database schema by running the Alembic migrations:

   ```
   python -m alembic upgrade head
   ```

6. **Set Up Google API Credentials**

   - Go to the Google Cloud Console.
   - Create a new project or select an existing one.
   - Enable the Gmail API for your project.
   - Create OAuth 2.0 credentials and download the `credentials.json` file.
   - Place the `credentials.json` file in the root of the project directory.

7. **Run the Application**

   You can now run the application using the following command:

   ```
   python -m src.gmail_automation.main
   ```

   Follow the prompts to authenticate with your Google account and start fetching emails.

## Testing

To run the tests, use the following command:

```
nox -s test
```

This will execute all unit and integration tests to ensure everything is functioning correctly.

## Additional Information

For more details on configuration options, refer to `docs/configuration.md`. For API integration specifics, check `docs/api.md`.