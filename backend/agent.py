from backend.llm_utils import generate_gemini_response
from backend import calendar_utils
import datetime
import re
import json
import pytz

# Simple intent extraction (for demo purposes)
def extract_intent_and_params(user_message: str):
    """
    Use Gemini to extract intent and parameters from the user message.
    For a production system, use function calling or a more robust approach.
    """
    prompt = f"""
    You are an assistant for booking Google Calendar appointments. 
    Given the following user message, extract:
    - intent (book, check_availability, suggest_slots)
    - date (YYYY-MM-DD or 'today', 'tomorrow', etc.)
    - time (HH:MM or time range)
    - duration (in minutes, if mentioned)
    - summary (meeting title, if mentioned)
    - description (if mentioned)
    Reply with ONLY a JSON object, no explanation or markdown.
    User message: {user_message}
    """
    gemini_response = generate_gemini_response(prompt)
    print("Gemini raw response:", gemini_response)
    # Try to extract JSON from Gemini's response
    try:
        # Remove markdown code block if present
        cleaned = gemini_response.strip()
        if cleaned.startswith('```json'):
            cleaned = cleaned[len('```json'):].strip()
        if cleaned.startswith('```'):
            cleaned = cleaned[len('```'):].strip()
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3].strip()
        data = json.loads(cleaned)
    except Exception as e:
        print(f"JSON extraction error: {e}")
        data = {}
    return data

def handle_user_message(user_message: str) -> str:
    data = extract_intent_and_params(user_message)
    intent = data.get('intent')
    date = data.get('date')
    time_str = data.get('time')
    duration = data.get('duration')
    summary = data.get('summary')
    description = data.get('description')

    # Parse date and time
    if date:
        if date.lower() == 'today':
            date_obj = datetime.date.today()
        elif date.lower() == 'tomorrow':
            date_obj = datetime.date.today() + datetime.timedelta(days=1)
        else:
            try:
                date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            except Exception:
                date_obj = None
    else:
        date_obj = None

    # Parse time
    if time_str and date_obj:
        try:
            if '-' in time_str:
                # Time range (e.g., 10:00-10:30)
                start_str, end_str = time_str.split('-')
                start_dt = IST.localize(datetime.datetime.combine(date_obj, datetime.datetime.strptime(start_str.strip(), '%H:%M').time()))
                end_dt = IST.localize(datetime.datetime.combine(date_obj, datetime.datetime.strptime(end_str.strip(), '%H:%M').time()))
            else:
                start_dt = IST.localize(datetime.datetime.combine(date_obj, datetime.datetime.strptime(time_str.strip(), '%H:%M').time()))
                if duration:
                    end_dt = start_dt + datetime.timedelta(minutes=int(duration))
                else:
                    end_dt = start_dt + datetime.timedelta(minutes=30)
        except Exception:
            start_dt = end_dt = None
    else:
        start_dt = end_dt = None

    # Handle intents
    if intent == 'check_availability' and start_dt and end_dt:
        available = calendar_utils.check_availability(start_dt, end_dt)
        if available:
            return f"The time slot {start_dt.strftime('%Y-%m-%d %H:%M')} to {end_dt.strftime('%H:%M')} is available."
        else:
            return f"Sorry, that time slot is not available."
    elif intent == 'suggest_slots' and date_obj and duration:
        slots = calendar_utils.suggest_slots(date_obj, int(duration))
        if slots:
            slot_strs = [f"{s[0].strftime('%H:%M')} - {s[1].strftime('%H:%M')}" for s in slots]
            return f"Available slots on {date_obj.strftime('%Y-%m-%d')}: {', '.join(slot_strs)}"
        else:
            return f"No available slots found on {date_obj.strftime('%Y-%m-%d')}."
    elif intent == 'book' and start_dt and end_dt and summary:
        event = calendar_utils.book_appointment(start_dt, end_dt, summary, description)
        event_link = event.get('htmlLink')
        return f"Booked '{summary}' on {start_dt.strftime('%Y-%m-%d %H:%M')} to {end_dt.strftime('%H:%M')}. [View in Google Calendar]({event_link})"
    else:
        return "Sorry, I couldn't understand your request. Please provide more details."

IST = pytz.timezone('Asia/Kolkata')
