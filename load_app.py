import imaplib
import email
from email.header import decode_header

# Define your credentials
username = "financeiro@lfleiloes.com.br"
password = "@Paodeleite0"  # Use an app password if 2FA is enabled

# Connect to the Gmail IMAP server
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# Log in to the account
try:
    imap.login(username, password)
    print("Login successful.")
except imaplib.IMAP4.error as e:
    print(f"Login failed: {str(e)}")

# List all mailboxes/folders
status, mailboxes = imap.list()
if status == "OK":
    print("Mailboxes:")
    for mailbox in mailboxes:
        print(mailbox.decode())

# Select the mailbox you want to interact with (e.g., "INBOX")
imap.select("INBOX")

# Search for all emails in the inbox
status, messages = imap.search(None, "ALL")

# Fetch and display the first email's subject
if status == "OK":
    mail_ids = messages[0].split()
    latest_email_id = mail_ids[-1]  # Get the latest email
    status, msg_data = imap.fetch(latest_email_id, "(RFC822)")
    if status == "OK":
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Decode the email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        print("Subject:", subject)

# Log out and close the connection
imap.logout()
