import asyncio
from src.gmail_automation.auth.gmail_auth import authenticate
from src.gmail_automation.gmail.fetcher import fetch_emails
from src.gmail_automation.database.connection import get_async_session
from src.gmail_automation.database.models import Email

async def main():
    # Authenticate and get the Gmail API service
    service = await authenticate()

    # Fetch emails from the Gmail API
    emails = await fetch_emails(service)

    async with get_async_session() as session:
        for email in emails:
            # Create an Email instance and add it to the session
            email_instance = Email(
                message_id=email['id'],
                thread_id=email['threadId'],
                subject=email['subject'],
                sender=email['from'],
                recipients=email['to'],
                body=email['body'],
                received_date=email['date'],
                labels=email['labels'],
                read_status=email['readStatus']
            )
            session.add(email_instance)

        # Commit the session to save emails to the database
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())