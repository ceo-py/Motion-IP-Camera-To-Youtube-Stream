import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import YOUTUBE
from utils import print_message


# --- Configuration ---
SCOPES = YOUTUBE["SCOPES"]
CLIENT_SECRETS_FILE = YOUTUBE["CLIENT_SECRETS_FILE"]
API_SERVICE_NAME = YOUTUBE["API_SERVICE_NAME"]
API_VERSION = YOUTUBE["API_VERSION"]
TOKEN_FILE = YOUTUBE["TOKEN_FILE"]


def save_token(credentials):
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(credentials, token)


def get_authenticated_service():
    """
    Authenticates the user and returns a YouTube service object.
    It manages the token.json file automatically after the first run.
    Uses run_local_server with specific messages for headless operation.
    """
    credentials = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)

    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)

        auth_url, _ = flow.authorization_url(prompt='consent')
        print_message(
            f"Please visit this URL to authorize this application:\n{auth_url}")

        try:
            credentials = flow.run_local_server(port=0, open_browser=False)
        except Exception as e:
            print_message(
                f"\nCould not run local server for auth. Ensure you have a GUI browser available if running locally.\nError: {e}")
            # Provide manual instructions as a fallback
            auth_url, _ = flow.authorization_url(prompt='consent')
            print_message(f"\nVisit this URL manually: {auth_url}\n")
            code = input(
                "Enter the authorization code from the redirected URL: ")
            flow.fetch_token(code=code)
            credentials = flow.credentials
            save_token(credentials)

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


if __name__ == '__main__':
    youtube = get_authenticated_service()

    print_message("\nAuthentication successful. You can now write functions to manage playlists.")