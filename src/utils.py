from datetime import datetime
from pathlib import Path
from config import YOUTUBE
import os

THUMBNAIL_PATH = YOUTUBE.get("THUMBNAIL_PATH")

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

def find_file_by_name(partial_name: str, search_dir=THUMBNAIL_PATH) -> str:
    """
    Search for a file that contains the partial name in its filename.
    Returns the full path of the matching file, or None if not found.
    """
    search_path = Path(search_dir)
    
    for file in search_path.rglob(f"*{partial_name}*"):
        if file.is_file():
            return file
    
    return None

def save_picture(cv2, frame, camera_name):
    # Save image when target detected
    os.makedirs(f"{THUMBNAIL_PATH}/images", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_path = os.path.join(f"{THUMBNAIL_PATH}/images", f"{camera_name}-{timestamp}.png")
    cv2.imwrite(image_path, frame)


def delete_file(file_path: str):
    """
    Delete a file given its full path.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print_message(f"THUMBNAIL DELETED {file_path.split("/")[-1]}")
    except Exception as e:
        print_message(f"Error deleting file: {e}")
