# main.py

from fastapi import FastAPI
from models import EventRequest # Importing EventRequest model
from google_calendar import list_events, create_event

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Google Calendar AI Agent Backend is running"}

@app.get("/events")
def get_calendar_events():
    return list_events()

@app.post("/events")
def book_event(event: EventRequest):
    event_payload = {
        "summary": event.summary,
        "description": event.description,
        "start": {"dateTime": event.start_time, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": event.end_time, "timeZone": "Asia/Kolkata"},
        "location": event.location,
    }
    return create_event(event_data=event_payload)
