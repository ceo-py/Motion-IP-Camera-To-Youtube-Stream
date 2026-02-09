import urllib.request
import urllib.error
import datetime
import json
import sys
from utils import print_message

# --- Import Configuration ---
try:
    from config import CAMERA_CONFIG
except ImportError:
    print_message("Error: Could not find 'config.py'. Ensure it's in the same directory.")
    sys.exit(1)

def send_webhook(CAMERA_NAME: str, video_link: str, target_found: str) -> None:
    if CAMERA_NAME not in CAMERA_CONFIG:
        print_message(f"Error: Camera '{CAMERA_NAME}' not defined in config.py.")
        sys.exit(1)

    if "WEBHOOK_URL" not in CAMERA_CONFIG[CAMERA_NAME] or not CAMERA_CONFIG[CAMERA_NAME]["WEBHOOK_URL"]:
        print_message(f"Error: Camera '{CAMERA_CONFIG[CAMERA_NAME]}' WEBHOOK_URL not defined in config.py.")
        sys.exit(1)

    if "MESSAGE" not in CAMERA_CONFIG[CAMERA_NAME] or not CAMERA_CONFIG[CAMERA_NAME]["MESSAGE"]:
        print_message(f"Error: Camera '{CAMERA_CONFIG[CAMERA_NAME]}' MESSAGE not defined in config.py.")
        sys.exit(1)

    # Construct the final message content
    CURRENT_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    FINAL_MESSAGE = f'{CAMERA_CONFIG[CAMERA_NAME]["MESSAGE"]} [{CURRENT_TIME}]({video_link}) {target_found}'
    DISCORD_WEBHOOK_URL = CAMERA_CONFIG[CAMERA_NAME]["WEBHOOK_URL"]

    payload = {
        "content": FINAL_MESSAGE
    }

    try:
        print_message(f"Sending Discord alert for {CAMERA_NAME}: '{FINAL_MESSAGE}'")

        # Assign the webhook URL to a local variable for clarity
        webhook_url = DISCORD_WEBHOOK_URL

        # 1. Encode the payload to bytes
        data = json.dumps(payload).encode('utf-8')

        # 2. Define headers, including Content-Type and User-Agent
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0' # Added User-Agent as per suggestion
        }

        # 3. Create the request object
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers=headers,
            method='POST'
        )

        # 4. Send the request (with a timeout)
        with urllib.request.urlopen(req, timeout=10) as response:
            # Discord returns 204 No Content on successful message post
            if response.getcode() == 204:
                print_message(f"SUCCESS: Discord message sent.")
            else:
                # Handle unexpected success codes
                print_message(f"INFO: Message sent, but unexpected status code: {response.getcode()}")

    except urllib.error.HTTPError as e:
        # Handles 4xx or 5xx errors from the server
        print_message(f"ERROR: Failed to send Discord message. Status Code: {e.code}")
        # print_message(f"Response Text: {e.read().decode('utf-8')}") # Uncomment for debugging

    except urllib.error.URLError as e:
        # Handles network issues (e.g., connection refused, DNS errors, timeout)
        print_message(f"ERROR: Network or connection error while sending Discord message: {e.reason}")