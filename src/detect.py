import requests
from utils import print_message
from config import DETECT_ENDPOINT

def is_target_present(rtsp_url: str) -> str | None:
    # Send a GET request with the rtsp_url as a query parameter
    response = requests.get(f"{DETECT_ENDPOINT}{rtsp_url}")
    
    if response.status_code == 200:

        api_message = response.json().get('message', 'No message provided')

        if "No human detected." in api_message:
            return None
        
        return f'Detected: {", ".join(api_message)}!'
    else:
        print_message(f"Error: {response.status_code} - {response.text}")
        return None
