import datetime
from typing import List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build


SERVICE_ACCOUNT_FILE = 'backend/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Replace with your calendar ID (can be your email or a calendar's ID)
CALENDAR_ID = 'gyanranjan4427@gmail.com'  

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service

def check_availability(start: datetime.datetime, end: datetime.datetime) -> bool:
    """Check if the calendar is free between start and end."""
    service = get_calendar_service()
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start.isoformat() + 'Z',
        timeMax=end.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime',
    ).execute()
    events = events_result.get('items', [])
    return len(events) == 0

def suggest_slots(date: datetime.date, duration_minutes: int, window_start: int = 9, window_end: int = 17) -> List[tuple]:
    """Suggest available slots on a given date within working hours (default 9am-5pm)."""
    service = get_calendar_service()
    slots = []
    start_time = datetime.datetime.combine(date, datetime.time(hour=window_start))
    end_time = datetime.datetime.combine(date, datetime.time(hour=window_end))
    current = start_time
    while current + datetime.timedelta(minutes=duration_minutes) <= end_time:
        slot_end = current + datetime.timedelta(minutes=duration_minutes)
        if check_availability(current, slot_end):
            slots.append((current, slot_end))
        current += datetime.timedelta(minutes=30)  # check every 30 minutes
    return slots

def book_appointment(start: datetime.datetime, end: datetime.datetime, summary: str, description: Optional[str] = None) -> dict:
    """Book an appointment on the calendar."""
    service = get_calendar_service()
    event = {
        'summary': summary,
        'description': description or '',
        'start': {'dateTime': start.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    print(f"Booked event: {created_event.get('htmlLink')}")
    return created_event
