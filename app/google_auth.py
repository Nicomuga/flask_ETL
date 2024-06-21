from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

def authenticate_google_drive():
    credentials_file = os.getenv('GOOGLE_DRIVE_CREDENTIALS_FILE')

    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, ['https://www.googleapis.com/auth/drive'])
    creds = flow.run_local_server(port=0)
    service = build('drive', 'v3', credentials=creds)

    return service
