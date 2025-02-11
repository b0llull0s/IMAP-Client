import imaplib
import email
from email import policy
from email.parser import BytesParser

# IMAP server settings (replace with your op.pl IMAP server details)
IMAP_SERVER = 'imap.poczta.onet.pl'
IMAP_PORT = 993  # Standard IMAP over SSL port
EMAIL = 'email'
PASSWORD = 'password'

def encode_mutf7(s):
    """
    Encode a string to MUTF-7 (Modified UTF-7) for IMAP folder names.
    """
    if s is None:
        raise ValueError("Folder name cannot be None.")
    return s.encode('utf-7').replace(b'+', b'&').replace(b'/', b',')

def connect_to_imap():
    # Connect to the IMAP server
    print(f"Connecting to {IMAP_SERVER} on port {IMAP_PORT}...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    print("Connected to IMAP server.")

    # Log in
    print(f"Logging in as {EMAIL}...")
    mail.login(EMAIL, PASSWORD)
    print("Login successful.")
    return mail

def fetch_emails(mail, mailbox='Społeczności'):
    try:
        # Verify the mailbox name
        if mailbox is None:
            raise ValueError("Mailbox name cannot be None.")

        # Encode the mailbox name in MUTF-7
        print(f"Original mailbox name: {mailbox}")
        mailbox_encoded = encode_mutf7(mailbox)
        print(f"Encoded mailbox name: {mailbox_encoded}")

        # Select the mailbox (e.g., Społeczności)
        print(f"Selecting mailbox: {mailbox}")
        status, response = mail.select(mailbox_encoded)
        if status != 'OK':
            print(f"Failed to select mailbox {mailbox}. Response: {response}")
            return

        # Search for all emails in the mailbox
        status, messages = mail.search(None, 'ALL')
        if status != 'OK':
            print("No emails found.")
            return

        # Get the list of email IDs
        email_ids = messages[0].split()
        print(f"Found {len(email_ids)} emails in {mailbox}.")

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
    except Exception as e:
        print(f"Error fetching emails: {e}")

def main():
    mail = connect_to_imap()
    try:
        fetch_emails(mail, mailbox='Społeczności')  # Specify the folder here
    finally:
        mail.logout()

if __name__ == '__main__':
    main()
