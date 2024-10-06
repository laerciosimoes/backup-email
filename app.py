import imaplib
import email
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()  # take environment variables from .env.

source_server = os.getenv("source_server")
source_email = os.getenv("source_email")
source_password = os.getenv("source_password")
source_map = os.getenv("source_map")
#
# Destination server credentials
dest_server = os.getenv("dest_server")
dest_email = os.getenv("dest_email")
dest_password = os.getenv("dest_password")
dest_map = os.getenv("dest_map")

# Function to connect to an IMAP server
def connect_imap(server, email, password):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(email, password)
    return mail

# Fetch all emails from the source IMAP server
def fetch_emails(source_mail):
    source_mail.select("inbox")  # Select the inbox
    result, data = source_mail.search(None, "ALL")  # Fetch all email IDs
    
    if result == "OK":
        return data[0].split()  # Return list of email IDs
    else:
        print("Failed to retrieve emails.")
        return []

# Function to copy emails to the destination IMAP server
def copy_emails_to_destination(source_mail, dest_mail, email_ids):
    i = 0
    for email_id in tqdm(email_ids, desc="Copying emails"):
        if i > 3981:
            # Fetch email by ID from source
            result, data = source_mail.fetch(email_id, "(RFC822)")
        
            if result == "OK":
                raw_email = data[0][1]
                
                # Parse the raw email
                msg = email.message_from_bytes(raw_email)
                
                # Get the Date header
                email_date = msg['Date']
                
                # Append the email to the destination inbox
                # You can use imaplib.Time2Internaldate to convert to IMAP date format
                if email_date:
                    print(f"Email ID: {email_id} | Date: {email_date}")
                else:
                    print(f"Email ID: {email_id} | Date not found")
                # Append email to the destination inbox
                #dest_mail.append('INBOX', '', imaplib.Time2Internaldate(time.time()), raw_email)
            else:
                print(f"Failed to fetch email ID: {email_id}")
        i = i + 1

def main():

    print(f"Source Server: {source_server}")
    print(f"Destination Server: {dest_server}")
    print(f'Destination Email {dest_email}')
    print(f"Dest password: {dest_password}")
    # Connect to source and destination IMAP servers
    source_mail = connect_imap(source_server, source_email, source_password)
    dest_mail = connect_imap(dest_server, dest_email, dest_password)

    # Fetch emails from source serverping imap.your-email-server.com
    email_ids = fetch_emails(source_mail)

    # Copy emails to destination server
    copy_emails_to_destination(source_mail, dest_mail, email_ids)

    # Close connections
    source_mail.logout()
    dest_mail.logout()

if __name__ == "__main__":
    main()
