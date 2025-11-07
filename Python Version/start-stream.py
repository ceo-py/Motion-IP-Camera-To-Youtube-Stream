# start_stream.py
import os
import sys
import subprocess
from datetime import datetime
from webhook import send_webhook
# --- Import Configuration ---
try:
    # This imports CAMERA_CONFIG, LOG_DIR, and FFMPEG_BIN
    from config import CAMERA_CONFIG, LOG_DIR, FFMPEG_BIN
except ImportError:
    print("Error: Could not find 'config.py'. Ensure it's in the same directory.")
    sys.exit(1)

# Get camera name from command line argument
if len(sys.argv) < 2:
    print("Usage: python start_stream.py <CAMERA_NAME>")
    sys.exit(1)

CAMERA_NAME = sys.argv[1]

# --- Configuration & File Setup ---
if CAMERA_NAME not in CAMERA_CONFIG:
    print(f"Error: Camera '{CAMERA_NAME}' not defined in config.py.")
    sys.exit(1)

# Get the specific config for the camera
CAM_CONFIG = CAMERA_CONFIG[CAMERA_NAME]
STREAM_URL = CAM_CONFIG["STREAM_URL"]
YOUTUBE_KEY = CAM_CONFIG["YOUTUBE_KEY"]

# Define file paths
LOG_FILE = os.path.join(LOG_DIR, f"ffmpeg-{CAMERA_NAME}.log")
PID_FILE = os.path.join(LOG_DIR, f"ffmpeg-{CAMERA_NAME}.pid")

# Ensure log directory exists and is writable
os.makedirs(LOG_DIR, mode=0o775, exist_ok=True)


def log_message(message):
    """Simple function to write a timestamped message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{timestamp} - {message}"
    print(full_message)
    with open(LOG_FILE, 'a') as f:
        f.write(full_message + '\n')


# --- PID Check Logic ---
if os.path.exists(PID_FILE):
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())

        # Check if PID is active (os.kill(pid, 0) checks existence without signaling)
        os.kill(pid, 0)
        log_message(f"Stream already running for {CAMERA_NAME} (PID: {pid})")
        sys.exit(0)

    except ProcessLookupError:
        # Process is dead, but PID file exists (stale)
        log_message("Stale PID file found, removing...")
        os.remove(PID_FILE)
    except Exception as e:
        log_message(f"Error checking PID file: {e}")


# --- Start FFmpeg Stream ---

# The full command list for subprocess
ffmpeg_command = [
    FFMPEG_BIN,
    '-rtsp_transport', 'tcp',
    '-i', STREAM_URL,
    '-c', 'copy', # Highly efficient, no re-encoding
    '-f', 'flv',
    f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_KEY}"
]

try:
    # Use subprocess.Popen for non-blocking, background execution.
    # stdout and stderr are redirected to the log file.
    with open(LOG_FILE, 'a') as log_f:
        process = subprocess.Popen(
            ffmpeg_command,
            stdout=log_f,
            stderr=subprocess.STDOUT, # Direct stderr to the same log file
            start_new_session=True    # Important: Decouples the process from the script's terminal
        )

    # Save process ID
    pid = process.pid
    with open(PID_FILE, 'w') as f:
        f.write(str(pid))

    log_message(f"Successfully started YouTube stream for {CAMERA_NAME} (PID: {pid})")
    log_message(f"Stream is using YouTube key: {YOUTUBE_KEY}")

    # You can now integrate your Discord message logic here, using the CHAT_INFO variable
    # print(f"\nDiscord Action: Preparing message for channel '{CHAT_INFO}'...")

except Exception as e:
    log_message(f"FATAL ERROR starting stream: {e}")
    # Clean up PID file if creation failed
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

send_webhook(CAMERA_NAME)
# Example Usage:
# python start_stream.py Kitchen