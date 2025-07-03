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
git clone <your-repo-url>
cd appointment-booking-api
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

## 🌐 Deployment (Railway/Render/Fly.io)

### Backend (FastAPI)
- Use the provided `Procfile`:
  ```
  web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
  ```
- Set environment variables (`GEMINI_API_KEY`)
- Upload `service_account.json` as a secret file (never commit to GitHub)

### Frontend (Streamlit)
- Use the provided `Procfile-streamlit` (rename to `Procfile`):
  ```
  web: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
  ```
- In `frontend/app.py`, set `BACKEND_URL` to your deployed backend's public URL

---

## 💬 Usage
- Open the Streamlit app
- Chat with the bot (e.g., "Book a meeting tomorrow at 3pm for 30 minutes called Project Sync")
- The bot will check availability, book the event, and return a link to the event in Google Calendar


## 📝 License
MIT
