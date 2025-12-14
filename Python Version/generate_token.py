import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# --- Configuration ---
SCOPES = ['https://www.googleapis.com/auth/youtube'] 
CLIENT_SECRETS_FILE = 'client_secret.json'
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    """
    Authenticates the user and returns a YouTube service object.
    It manages the token.json file automatically after the first run.
    Uses run_local_server with specific messages for headless operation.
    """
    credentials = None
    
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"Please visit this URL to authorize this application:\n{auth_url}")
            
            try:
                credentials = flow.run_local_server(port=0, open_browser=False)
            except Exception as e:
                print(f"\nCould not run local server for auth. Ensure you have a GUI browser available if running locally.\nError: {e}")
                # Provide manual instructions as a fallback
                auth_url, _ = flow.authorization_url(prompt='consent')
                print(f"\nVisit this URL manually: {auth_url}\n")
                code = input("Enter the authorization code from the redirected URL: ")
                flow.fetch_token(code=code)
                credentials = flow.credentials


        with open('token.json', 'wb') as token:
            pickle.dump(credentials, token)
            
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

if __name__ == '__main__':
    youtube = get_authenticated_service()
    
    print("\nAuthentication successful. You can now write functions to manage playlists.")
