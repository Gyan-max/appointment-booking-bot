from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import datetime
from . import calendar_utils

app = FastAPI()

class AvailabilityRequest(BaseModel):
    start: datetime.datetime
    end: datetime.datetime

class SuggestSlotsRequest(BaseModel):
    date: datetime.date
    duration_minutes: int
    window_start: Optional[int] = 9
    window_end: Optional[int] = 17

class BookAppointmentRequest(BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    summary: str
    description: Optional[str] = None

@app.post("/check-availability")
def check_availability(req: AvailabilityRequest):
    available = calendar_utils.check_availability(req.start, req.end)
    return {"available": available}

@app.post("/suggest-slots")
def suggest_slots(req: SuggestSlotsRequest):
    slots = calendar_utils.suggest_slots(req.date, req.duration_minutes, req.window_start, req.window_end)
    # Convert datetime objects to isoformat for JSON serialization
    slots_serialized = [(s[0].isoformat(), s[1].isoformat()) for s in slots]
    return {"slots": slots_serialized}

@app.post("/book-appointment")
def book_appointment(req: BookAppointmentRequest):
    try:
        event = calendar_utils.book_appointment(req.start, req.end, req.summary, req.description)
        return {"event": event}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
