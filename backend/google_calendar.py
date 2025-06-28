# google_calendar.py

import os
import pickle
from fastapi import HTTPException
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from dotenv import load_dotenv
load_dotenv()


SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE = "token_calendar.pickle"
CREDENTIALS_FILE = os.getenv("GOOGLE_CLIENT_SECRET", "client_secret.json")

def get_credentials():
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                auth_url, _ = flow.authorization_url(prompt='consent')
                with open(TOKEN_FILE, "wb") as token:
                    pickle.dump(creds, token)
            except Exception as e:
                raise HTTPException(status_code=401, detail=str(e))

    return creds

def get_calendar_service():
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds, static_discovery=False)

def list_events(calendar_id="primary"):
    service = get_calendar_service()
    events_result = service.events().list(calendarId=calendar_id, maxResults=10).execute()
    return events_result.get("items", [])

from typing import Dict, Any

def create_event(calendar_id: str = "primary", event_data: Dict[str, Any] = {}):
    service = get_calendar_service()
    event = service.events().insert(calendarId=calendar_id, body=event_data).execute()
    return event
