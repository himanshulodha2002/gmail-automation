# Setup Instructions for Gmail Automation Project

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.8 or higher
- SQLite3 (default, no setup needed)
- [uv](https://github.com/astral-sh/uv) (modern Python package manager)

## Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/gmail-automation.git
   cd gmail-automation
   ```

2. **Install `uv`**

   ```bash
   # On macOS & Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Create Virtual Environment and Install Dependencies**

   ```bash
   make install
   ```

4. **Set Up Google API Credentials**

   - Go to the Google Cloud Console.
   - Create a new project or select an existing one.
   - Enable the Gmail API for your project.
   - Create OAuth 2.0 credentials and download the `credentials.json` file.
   - Place the `credentials.json` file in the root of the project directory.

5. **Configure Environment Variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Initialize the Database**

   ```bash
   make setup-db
   ```

7. **Fetch Emails**

   ```bash
   make fetch
   ```

8. **Process Emails with Rules**

   ```bash
   make process-rules
   ```

## Additional Information

- The SQLite database is stored in the `data/` directory and is gitignored.
- The rules file is located at `config/rules.json`.
- For more configuration options, see `docs/configuration.md`.
