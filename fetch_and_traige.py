# fetch_and_triage.py

import os
from dotenv import load_dotenv
import imaplib
import email
from email import policy
from email.utils import parseaddr
from email.header import decode_header
import requests

def extract_sender_email(raw_email):
    message = email.message_from_bytes(raw_email, policy=policy.default)
    from_header = message['From']
    sender_email = parseaddr(from_header)[1]
    return sender_email


# Step 1: Load credentials
load_dotenv()
EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = int(os.getenv("IMAP_PORT", 993))  # Default to 993 if not provided

# Step 2: Fetch and triage emails
def fetch_latest_emails(n=5):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # Get list of email IDs
    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()[-n:]

    for eid in email_ids:
        result, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        sender_email = extract_sender_email(raw_email)

        subject, _ = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        print(f"\n📩 Subject: {subject}")
        print(f"📨 From: {sender_email}")
        print(f"📝 Body Preview: {body[:200]}...")


        # Step 3: Send to triage endpoint
        response = requests.post("http://localhost:8000/triage", json={"email": body, "sender_email": sender_email})
        print(f"✅ Triage Result: {response.json()}")

    mail.logout()

# Step 4: Run
if __name__ == "__main__":
    fetch_latest_emails(n=5)
