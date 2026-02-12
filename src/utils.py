from datetime import datetime

def print_message(message: str):
    """Simple function to print a timestamped message to the console."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{timestamp} - {message}"
    print(full_message, flush=True)

def find_camera_key(stream_url: str, CAMERA_CONFIG: dict):
    for key in CAMERA_CONFIG:
        if CAMERA_CONFIG[key].get("STREAM_URL") == stream_url:
            return key
    return None