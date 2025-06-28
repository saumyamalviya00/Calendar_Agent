
import os
import pickle
import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def create_service(client_secrets_file, api_name, api_version, *scopes, prefix=''):
    SCOPES = [scope for scope in scopes]
    creds = None
    token_file = f'token_{api_name}_{api_version}{prefix}.pickle'

    # Try loading existing token
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If no valid token, start the OAuth flow
    if not creds or not creds.valid:
        flow = Flow.from_client_secrets_file(
            client_secrets_file=client_secrets_file,
            scopes=SCOPES,
            redirect_uri="https://CalendarAgent.streamlit.app"
        )

        auth_url, _ = flow.authorization_url(prompt='consent')

        st.markdown(f"**👉 [Click here to authorize with Google Calendar]({auth_url})**")

        redirect_response = st.text_input("Paste the full URL you were redirected to here:")

        if redirect_response:
            try:
                flow.fetch_token(authorization_response=redirect_response)
                creds = flow.credentials
                # Save token
                with open(token_file, 'wb') as token:
                    pickle.dump(creds, token)
            except Exception as e:
                st.error(f"Authorization failed: {e}")
                return None

    try:
        service = build(api_name, api_version, credentials=creds, static_discovery=False)
        return service
    except Exception as e:
        st.error(f"Failed to create Google API service: {e}")
        return None
