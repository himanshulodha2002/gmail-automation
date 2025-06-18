# Gmail Automation

A clean and modern Python project that connects to the Gmail API and processes emails using rule-based logic.

## Features

- 🔐 OAuth2 authentication with Gmail API
- 📧 Fetch emails using Gmail REST API
- 💾 Store emails in SQLite database
- 📋 Rule-based email processing with JSON configuration
- 🎯 Actions: mark as read/unread, move messages

## Setup

1. **Install dependencies with uv:**

   ```bash
   uv sync
   ```

2. **Google API Setup:**

   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing one
   - Enable Gmail API
   - Create OAuth2 credentials (Desktop application)
   - Download `credentials.json` and place in project root

3. **Environment Setup:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Usage

1. **Fetch emails from Gmail:**

   ```bash
   uv run fetch-emails
   ```

2. **Process emails with rules:**

   ```bash
   uv run process-rules
   ```

3. **Run with custom rules file:**
   ```bash
   uv run process-rules --rules custom_rules.json
   ```

## Rule Configuration

Edit `rules.json` to define your email processing rules:

```json
{
  "rules": [
    {
      "name": "Mark promotional emails as read",
      "conditions": [
        {
          "field": "from",
          "predicate": "contains",
          "value": "noreply"
        }
      ],
      "logic": "any",
      "actions": [
        {
          "type": "mark_read"
        }
      ]
    }
  ]
}
```

## Development

- **Linting:** `uv run ruff check`
- **Testing:** `uv run pytest`
- **Format:** `uv run ruff format`

## Project Structure

```
gmail-automation/
├── src/gmail_automation/     # Main package
├── scripts/                  # Entry point scripts
├── tests/                    # Unit tests
├── rules.json               # Rule definitions
└── credentials.json         # Google OAuth credentials
```

├── tests/ # Unit tests
├── rules.json # Rule definitions
└── credentials.json # Google OAuth credentials

```

```
