import os.path
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from smolagents import tool

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(sender, to, subject, message_text):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message.attach(MIMEText(message_text, 'plain'))
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(subject: str, body: str, reciever: str):
    service = get_gmail_service()
    sender = "candidatedemo470@gmail.com"

    message = create_message(sender, reciever, subject, body)
    try:
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Message sent! ID: {sent_message['id']}")
    except Exception as error:
        print(f"An error occurred: {error}")

        
@tool
def reply_email(subject: str, body: str, receiver: str) -> str:
    """
    Sends a follow-up email to an applicant requesting clarification or additional information.

    This tool is used to contact applicants whose qualifications require further assessment.
    The email should contain specific questions or points that need clarification, such as missing
    documents, inconsistencies in the application, or unclear academic/work history. Applicants are
    expected to respond with the requested information and re-submit their updated application materials.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email, including specific questions or clarification requests.
        receiver (str): The recipient's email address (the applicant).

    Returns:
        str: Result message indicating success or failure.
    """
    try:
        send_email(subject, body, receiver)
        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email: {str(e)}"
