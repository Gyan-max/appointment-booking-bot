# Appointment Booking Bot

## 📅 Description
A conversational AI agent that helps users book appointments directly into their Google Calendar through a natural chat interface. The agent understands user intent, checks calendar availability, suggests suitable time slots, and confirms bookings—all via chat!

---

## 🚀 Features
- Conversational chat interface (Streamlit)
- Google Calendar integration (Service Account, no OAuth needed)
- Checks availability, suggests slots, and books appointments
- Returns a direct link to the booked event
- Powered by Gemini LLM for natural language understanding
- FastAPI backend for API endpoints

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI
- **Agent:** Langchain, Gemini LLM (Google Generative AI)
- **Frontend:** Streamlit
- **Calendar Integration:** Google Calendar API (Service Account)

---

## ⚡ Quick Start (Local)

### 1. Clone the repository
```bash
git clone https://github.com/Gyan-max/appointment-booking-bot.git
cd appointment-booking-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up Google Service Account
- Create a service account in Google Cloud Console
- Enable Google Calendar API
- Download the JSON key and place it at `backend/service_account.json`
- Share your Google Calendar with the service account email ("Make changes to events")
- Set `CALENDAR_ID` in `backend/calendar_utils.py` to your calendar's ID (e.g., your Gmail address)

### 4. Set up Gemini API Key
- Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create a `.env` file in the project root:
  ```
  GEMINI_API_KEY=your-gemini-api-key-here
  ```

### 5. Run the backend
```bash
uvicorn backend.main:app --reload
```

### 6. Run the frontend
```bash
streamlit run frontend/app.py
```

---



## 📝 License
MIT
