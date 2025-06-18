# Gmail API Integration Documentation

## Overview
This document provides an overview of the Gmail API integration within the Gmail Automation project. It outlines the key functionalities, authentication process, and how to interact with the API to fetch emails.

## Authentication
The Gmail API requires OAuth 2.0 for authentication. The project implements the OAuth flow using the `gmail_auth.py` module. Follow these steps to authenticate:

1. **Create a Google Cloud Project**: 
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the Gmail API.

2. **Set Up OAuth Consent Screen**: 
   - Configure the OAuth consent screen with the necessary information.

3. **Create Credentials**: 
   - Generate OAuth 2.0 credentials (Client ID and Client Secret).
   - Download the credentials JSON file and place it in the project directory.

4. **Run the Authentication Script**: 
   - Execute the authentication script to obtain and store the access token.

## Fetching Emails
Once authenticated, you can fetch emails using the Gmail API. The `fetcher.py` module handles the email fetching logic. Key functionalities include:

- **Batch Fetching**: Retrieve emails in batches to optimize performance.
- **Pagination**: Handle pagination to fetch all emails.
- **Rate Limiting**: Implement rate limiting to comply with Gmail API usage policies.

### Example Usage
To fetch emails, call the `fetch_emails` function from the `fetcher.py` module. This function will return a list of emails based on the defined criteria.

## Rule Engine
The project includes a rule engine that processes emails based on user-defined rules. Rules are defined in a JSON format and can include conditions and actions.

### Rule Structure
Each rule consists of:
- **Conditions**: Criteria to evaluate against the fetched emails (e.g., sender, subject).
- **Actions**: Operations to perform when conditions are met (e.g., mark as read, move message).

### Example Rule
```json
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
```

## Logging
The project uses structured logging to track API interactions and errors. The logging configuration is defined in `logging.yaml`.

## Conclusion
This document serves as a guide for integrating and using the Gmail API within the Gmail Automation project. For further details on configuration and setup, refer to the `setup.md` and `configuration.md` documents.