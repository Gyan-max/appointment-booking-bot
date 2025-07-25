import streamlit as st
import requests
import os


BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Appointment Booking Chatbot", page_icon="📅")
st.title("📅 Appointment Booking Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown("Chat with the assistant to book, check, or suggest appointments on your Google Calendar.")

user_input = st.text_input("You:", "", key="user_input")

if st.button("Send") and user_input.strip():
    st.session_state["messages"].append(("user", user_input))
    # Send to backend
    try:
        response = requests.post(
            BACKEND_URL,
            json={"message": user_input},
            timeout=30
        )
        if response.status_code == 200:
            agent_reply = response.json().get("response", "(No response)")
        else:
            agent_reply = f"Error: {response.text}"
    except Exception as e:
        agent_reply = f"Error: {e}"
    st.session_state["messages"].append(("agent", agent_reply))
    # st.experimental_user()


for sender, msg in st.session_state["messages"]:
    if sender == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Agent:** {msg}")
