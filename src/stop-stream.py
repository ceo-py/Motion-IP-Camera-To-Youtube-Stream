# stop_stream.py
import os
import sys
import signal
import time
from utils import print_message
from youtube import go_end_stream
import subprocess




# --- Import Configuration ---
try:
    # This imports CAMERA_CONFIG and FFMPEG_BIN
    from config import CAMERA_CONFIG
except ImportError:
    print_message("Error: Could not find 'config.py'. Ensure it's in the same directory.")
    sys.exit(1)

# Get camera name from command line argument
if len(sys.argv) < 2:
    print_message("Usage: python stop_stream.py <CAMERA_NAME>")
    sys.exit(1)


CAMERA_NAME = sys.argv[1]

# --- Configuration & File Setup ---
if CAMERA_NAME not in CAMERA_CONFIG:
    print_message(f"[{CAMERA_NAME}] Error: Camera not defined in config.py.")
    sys.exit(1)

# Get the specific config for the camera
CAM_CONFIG = CAMERA_CONFIG[CAMERA_NAME]
YOUTUBE_KEY = CAM_CONFIG["YOUTUBE_KEY"]


def is_ffmpeg_streaming(pid: int) -> None:
    try:
        # 1. Attempt Graceful Stop (SIGTERM)
        print_message(f"[{CAMERA_NAME}] Attempting to gracefully stop FFmpeg (PID: {pid})")
        os.kill(pid, signal.SIGTERM)
        time.sleep(3)

        # 2. Check if the process is still alive (os.kill(pid, 0) is non-destructive)
        try:
            os.kill(pid, 0)

            # If still alive, Force Kill (SIGKILL)
            print_message(f"[{CAMERA_NAME}] Graceful stop failed. Force killing FFmpeg (PID: {pid})")
            os.kill(pid, signal.SIGKILL)

        except ProcessLookupError:
            print_message(f"[{CAMERA_NAME}] Successfully stopped FFmpeg (PID: {pid})")
            go_end_stream(CAMERA_NAME)


    except Exception as e:
        print_message(f"[{CAMERA_NAME}] Error while managing PID: {e}")


def stop_ffmpeg_stream():
    """Check if any ffmpeg process is running with the specified stream URL."""
    try:
        # Run ps to check for ffmpeg processes
        result = subprocess.run(
            ['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        # Search for the stream URL in the ffmpeg process list
        for line in result.stdout.splitlines():
            if 'ffmpeg' in line and YOUTUBE_KEY in line:
                pid = int(line.split()[1])
                is_ffmpeg_streaming(pid)
                return
        print_message(f"[{CAMERA_NAME}] No active stream is found.")
    except Exception as e:
        print(f"[{CAMERA_NAME}] Error checking ffmpeg process: {e}")

stop_ffmpeg_stream()