# stop_stream.py
import os
import sys
import signal
import time
from datetime import datetime

# --- Import Configuration ---
try:
    # This imports CAMERA_CONFIG, LOG_DIR, and FFMPEG_BIN
    from config import CAMERA_CONFIG, LOG_DIR
except ImportError:
    print("Error: Could not find 'config.py'. Ensure it's in the same directory.")
    sys.exit(1)

# Get camera name from command line argument
if len(sys.argv) < 2:
    print("Usage: python stop_stream.py <CAMERA_NAME>")
    sys.exit(1)

CAMERA_NAME = sys.argv[1]

# --- Check if the camera name is valid ---
if CAMERA_NAME not in CAMERA_CONFIG:
    print(f"Error: Camera '{CAMERA_NAME}' not defined in config.py.")
    sys.exit(1)

# Define file paths based on configuration constants
LOG_FILE = os.path.join(LOG_DIR, f"ffmpeg-{CAMERA_NAME}.log")
PID_FILE = os.path.join(LOG_DIR, f"ffmpeg-{CAMERA_NAME}.pid")

# Ensure log directory exists (if not created by the start script)
os.makedirs(LOG_DIR, exist_ok=True)


def log_message(message):
    """Simple function to write a timestamped message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{timestamp} - {message}"
    print(full_message)
    with open(LOG_FILE, 'a') as f:
        f.write(full_message + '\n')


# --- Stop Logic ---
if os.path.exists(PID_FILE):
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())

        # 1. Attempt Graceful Stop (SIGTERM)
        log_message(f"Attempting to gracefully stop FFmpeg for {CAMERA_NAME} (PID: {pid})")
        os.kill(pid, signal.SIGTERM)
        time.sleep(3)

        # 2. Check if the process is still alive (os.kill(pid, 0) is non-destructive)
        try:
            os.kill(pid, 0)

            # If still alive, Force Kill (SIGKILL)
            log_message(f"Graceful stop failed. Force killing FFmpeg (PID: {pid})")
            os.kill(pid, signal.SIGKILL)

        except ProcessLookupError:
            log_message(f"Successfully stopped FFmpeg for {CAMERA_NAME} (PID: {pid})")

    except Exception as e:
        log_message(f"Error while managing PID file: {e}")

    # Clean up the PID file
    os.remove(PID_FILE)

else:
    log_message(f"No PID file found for {CAMERA_NAME}. Stream may not be running.")

# Example Usage:
# python stop_stream.py Kitchen