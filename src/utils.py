from datetime import datetime
from pathlib import Path
from config import YOUTUBE
import os

THUMBNAIL_PATH = YOUTUBE.get("THUMBNAIL_PATH")
MAX_SIZE_BYTES = 1900 * 1024  # 1.9MB


def get_timestamp() -> str:
    """Get current timestamp in standard format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def draw_detect_objectcv(cv2, box, frame, label, conf):
    x1, y1, x2, y2 = map(int, box.xyxy[0])

    # Draw rectangle
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Draw label background
    text = f"{label} {conf:.2f}"
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    cv2.rectangle(frame, (x1, y1 - h - 10), (x1 + w, y1), (0, 255, 0), -1)

    # Draw label text
    cv2.putText(
        frame,
        text,
        (x1, y1 - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 0),
        2
    )

    return frame


def save_compressed_thumbnail(cv2, frame, output_path):
    # Resize first (very important)
    frame = cv2.resize(frame, (1280, 720))

    quality = 95

    while quality >= 20:
        success, encoded = cv2.imencode(
            ".jpg",
            frame,
            [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        )

        if not success:
            raise Exception("Failed to encode image")

        if len(encoded) <= MAX_SIZE_BYTES:
            # Write only once
            with open(output_path, "wb") as f:
                f.write(encoded.tobytes())

            print(f"Saved thumbnail at quality {quality}")
            return output_path

        quality -= 5

    raise Exception("Could not compress image under 2MB")


def save_picture(cv2, frame, camera_name):
    os.makedirs(f"{THUMBNAIL_PATH}/images", exist_ok=True)

    timestamp = get_timestamp()
    image_path = os.path.join(
        f"{THUMBNAIL_PATH}/images",
        f"{camera_name}-{timestamp}.jpg"
    )

    # Call the internal thumbnail compression function
    save_compressed_thumbnail(cv2, frame, image_path)


def print_message(message: str):
    """Simple function to print a timestamped message to the console."""
    timestamp = get_timestamp()
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


def delete_file(file_path: str):
    """Delete a file given its full path."""
    try:
        os.remove(file_path)
        filename = os.path.basename(file_path)
        print_message(f"THUMBNAIL DELETED {filename}")
    except FileNotFoundError:
        pass  # File already deleted
    except Exception as e:
        print_message(f"Error deleting file: {e}")