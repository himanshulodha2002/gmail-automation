# Gmail Automation

A clean and modern Python project that connects to the Gmail API and processes emails using rule-based logic.

## Features

- OAuth2 authentication with Gmail API
- Fetch emails using Gmail REST API
- Store emails in SQLite database (in `data/`)
- Rule-based email processing with JSON configuration
- Actions: mark as read/unread, move messages

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/himanshulodha2002/gmail-automation.git
   cd gmail-automation
   ```

2. **Install `uv`:**

   ```bash
   # On macOS & Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Create virtual environment and install dependencies:**

   ```bash
   make install
   ```

   **To install all optional dependencies:**

   ```bash
   make install --all-extras
   ```

4. **Set up Google Cloud project and OAuth 2.0:**

   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the Gmail API.
   - Create OAuth 2.0 credentials (Desktop app).
   - Download `credentials.json` and place it in the project root.

5. **Environment Setup:**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Initialize the database:**

   ```bash
   make setup-db
   ```

## Usage

1. **Fetch emails from Gmail:**

   ```bash
   make fetch
   ```

2. **Process emails with rules:**

   ```bash
   make process-rules
   ```

3. **Run with custom rules file:**

   ```bash
   uv run env PYTHONPATH=src python scripts/process_rules.py --rules custom_rules.json
   ```

## Rule Configuration

Edit `config/rules.json` to define your email processing rules:

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

To sync all optional dependencies:

```bash
uv sync --all-extras
```

- **Linting:** `make lint`
- **Testing:** `make test`
- **Format:** `make format`
- **Type checking:** `make type-check`

## Project Structure

```
gmail-automation/
├── src/gmail_automation/     # Main package
├── scripts/                  # Entry point scripts
├── data/                     # SQLite database (gitignored)
├── tests/                    # Unit tests
├── rules.json                # Rule definitions
├── credentials.json          # Google OAuth credentials
├── Makefile
└── README.md
```

## Video Demo

Watch a quick demo of Gmail Automation in action:

[Watch the demo, Hi-res](https://youtu.be/iJXP1p5nGoo)  
[Watch the demo](https://www.youtube.com/watch?v=8UStdgFXb_s)  
[Alternate demo](https://drive.google.com/drive/folders/1Ydu78MpyvQ4VzNkjljA9Ji5Kc5_N-OTQ?usp=sharing)

## Notes

- The SQLite database is stored in the `data/` directory and is gitignored.
- For more details, see `docs/setup.md` and `docs/configuration.md`.
