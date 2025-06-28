# streamlit_app.py

import os
import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import google.auth.transport.requests

# Point to your client_secret.json
CLIENT_SECRET_FILE = os.path.join("..", "credentials", "client_secret.json")

# Load secrets from Streamlit secrets.toml
client_id = st.secrets["google_oauth"]["client_id"]
client_secret = st.secrets["google_oauth"]["client_secret"]
redirect_uri = st.secrets["google_oauth"]["redirect_uri"]

SCOPES = ['https://www.googleapis.com/auth/calendar']
st.set_page_config(page_title="Google Calendar Chat Agent")
st.title("📅 AI Calendar Booking Agent")

# Session state for credentials
if "creds" not in st.session_state:
    st.session_state.creds = None

# Google OAuth Flow
if not st.session_state.creds:
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": [redirect_uri],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )

    auth_url, _ = flow.authorization_url(
        prompt='consent', access_type='offline', include_granted_scopes='true'
    )

    st.markdown(f"### 🔐 Please [Login with Google]({auth_url}) to continue.")

    # ✅ Replaced deprecated experimental API
    query_params = st.query_params
    if 'code' in query_params:
        try:
            flow.fetch_token(code=query_params['code'][0])
            st.session_state.creds = flow.credentials
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Authentication failed: {e}")

# After login
if st.session_state.creds:
    st.success("✅ Logged in with Google")
    service = build("calendar", "v3", credentials=st.session_state.creds)

    if "chat" not in st.session_state:
        st.session_state.chat = []

    # Display chat history
    for chat in st.session_state.chat:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # Accept user input
    if prompt := st.chat_input("How can I help you schedule?"):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Basic logic: view or book
        if "show" in prompt.lower():
            try:
                events = service.events().list(calendarId="primary", maxResults=5).execute()
                reply = "📅 Upcoming events:\n"
                for e in events.get("items", []):
                    start = e["start"].get("dateTime", e["start"].get("date"))
                    reply += f"- {e.get('summary','(No Title)')} at {start}\n"
            except Exception as e:
                reply = f"⚠️ Error fetching events: {e}"
        else:
            reply = "🤖 Try: 'show events' or 'book meeting'."

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.chat.append({"role": "assistant", "content": reply})
