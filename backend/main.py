from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import datetime
from . import calendar_utils
from .agent import handle_user_message

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://appointment-booking-bot-6qnr.onrender.com/"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def health_check():
    return {"status": "healthy"}

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

class ChatRequest(BaseModel):
    message: str

@app.post("/check-availability")
def check_availability(req: AvailabilityRequest):
    available = calendar_utils.check_availability(req.start, req.end)
    return {"available": available}

@app.post("/suggest-slots")
def suggest_slots(req: SuggestSlotsRequest):
    slots = calendar_utils.suggest_slots(req.date, req.duration_minutes, req.window_start, req.window_end)
   
    slots_serialized = [(s[0].isoformat(), s[1].isoformat()) for s in slots]
    return {"slots": slots_serialized}

@app.post("/book-appointment")
def book_appointment(req: BookAppointmentRequest):
    try:
        event = calendar_utils.book_appointment(req.start, req.end, req.summary, req.description)
        return {"event": event}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = handle_user_message(req.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
