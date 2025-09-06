import os
import base64
import tempfile
from datetime import datetime
from email.utils import parsedate_to_datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from state import State

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def detect_certificates(_: State) -> State:
    service = get_gmail_service()
    query = 'subject:("certificate" OR "achievement") newer_than:7d'
    results = service.users().messages().list(userId="me", q=query, maxResults=1).execute()
    messages = results.get("messages", [])

    if not messages:
        return {
            "certificate_title": "No recent certificate found",
            "program_name": "-",
        }

    msg = service.users().messages().get(userId="me", id=messages[0]["id"]).execute()
    headers = msg["payload"]["headers"]

    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "Certificate")
    date_header = next((h["value"] for h in headers if h["name"] == "Date"), None)

    if date_header:
        try:
            issued_date = parsedate_to_datetime(date_header).date().isoformat()
        except Exception:
            issued_date = datetime.utcnow().date().isoformat()
    else:
        issued_date = datetime.utcnow().date().isoformat()

    cert_image_path = None
    for part in msg.get("payload", {}).get("parts", []):
        filename = part.get("filename")
        body = part.get("body", {})
        if filename and ("pdf" in filename.lower() or filename.lower().endswith((".png", ".jpg", ".jpeg"))):
            att_id = body.get("attachmentId")
            if att_id:
                att = service.users().messages().attachments().get(
                    userId="me", messageId=msg["id"], id=att_id
                ).execute()
                data = att.get("data")
                if data:
                    file_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[-1]) as f:
                        f.write(file_data)
                        cert_image_path = f.name

    return {
        "certificate_title": subject,
        "program_name": "Program (from email)",
        "issued_on": issued_date,
        "cert_image_path": cert_image_path,
    }
