import imaplib
import email
from email import policy
from email.parser import BytesParser

# IMAP server settings (replace with your op.pl IMAP server details)
IMAP_SERVER = ''
IMAP_PORT = 993  # Standard IMAP over SSL port
EMAIL = 'your_email'
PASSWORD = 'your_password'

def connect_to_imap():
    try:
        # Connect to the IMAP server
        print(f"Connecting to {IMAP_SERVER} on port {IMAP_PORT}...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        print("Connected to IMAP server.")

        # Log in
        print(f"Logging in as {EMAIL}...")
        mail.login(EMAIL, PASSWORD)
        print("Login successful.")
        return mail
    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def fetch_emails(mail, mailbox='INBOX'):
    # Select the mailbox (e.g., INBOX)
    mail.select(mailbox)

    # Search for all emails in the mailbox
    status, messages = mail.search(None, 'ALL')
    if status != 'OK':
        print("No emails found.")
        return

    # Get the list of email IDs
    email_ids = messages[0].split()

    for e_id in email_ids:
        # Fetch the email by ID
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        if status != 'OK':
            print(f"Failed to fetch email {e_id}.")
            continue

        # Parse the raw email content
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = BytesParser(policy=policy.default).parsebytes(response_part[1])
                print(f"Subject: {msg['subject']}")
                print(f"From: {msg['from']}")
                print(f"Date: {msg['date']}")
                print("Body:")
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == 'text/plain':
                            print(part.get_payload(decode=True).decode())
                else:
                    print(msg.get_payload(decode=True).decode())
                print("-" * 40)

def main():
    try:
        mail = connect_to_imap()
        # Fetch emails (add your logic here)
    except Exception as e:
        print(f"Failed to connect or fetch emails: {e}")
    finally:
        if 'mail' in locals():
            mail.logout()

if __name__ == '__main__':
    main()
