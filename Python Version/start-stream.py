import sys
import subprocess
from webhook import send_webhook
from utils import print_message
from youtube import start_youtube_broadcast_stream
from detect import is_target_present

# --- Import Configuration ---
try:
    # This imports CAMERA_CONFIG and FFMPEG_BIN
    from config import CAMERA_CONFIG, FFMPEG_BIN
except ImportError:
    print_message("Error: Could not find 'config.py'. Ensure it's in the same directory.")
    sys.exit(1)

# Get camera name from command line argument
if len(sys.argv) < 2:
    print_message("Usage: python start_stream.py <CAMERA_NAME>")
    sys.exit(1)

CAMERA_NAME = sys.argv[1]

# --- Configuration & File Setup ---
if CAMERA_NAME not in CAMERA_CONFIG:
    print_message(f"Error: Camera '{CAMERA_NAME}' not defined in config.py.")
    sys.exit(1)

# Get the specific config for the camera
CAM_CONFIG = CAMERA_CONFIG[CAMERA_NAME]
STREAM_URL = CAM_CONFIG["STREAM_URL"]
YOUTUBE_KEY = CAM_CONFIG["YOUTUBE_KEY"]

# Check for human or animals
if not is_target_present(STREAM_URL):
    print_message("No Human/Animal found!!")
    sys.exit(0)

# --- PID Check Logic ---
# Check if ffmpeg is already running for the specific camera stream
def is_ffmpeg_streaming():
    try:
        result = subprocess.run(
            ['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        for line in result.stdout.splitlines():
            if 'ffmpeg' in line and STREAM_URL in line:
                print_message(f"Stream already running for {CAMERA_NAME} (process found).")
                return True
        return False
    except Exception as e:
        print_message(f"Error checking ffmpeg process: {e}")
        return False

# Check if the stream is already running
if is_ffmpeg_streaming():
    sys.exit(0)

# --- Start FFmpeg Stream ---
ffmpeg_command = [
    FFMPEG_BIN,
    '-rtsp_transport', 'tcp',
    '-i', STREAM_URL,
    '-c', 'copy',  # Highly efficient, no re-encoding
    '-f', 'flv',
    f"rtmps://a.rtmp.youtube.com/live2/{YOUTUBE_KEY}"
]

try:
    # Start the ffmpeg process in the background
    process = subprocess.Popen(
        ffmpeg_command,
        stdout=subprocess.PIPE,  # Capture standard output (stdout)
        stderr=subprocess.PIPE,  # Capture standard error (stderr)
        start_new_session=True    # Decouple process from the terminal
    )
    pid = process.pid
    # Print success message after starting the stream
    print_message(f"Successfully started YouTube stream for {CAMERA_NAME} (PID: {pid}).")
    print_message(f"Stream is using YouTube key: {YOUTUBE_KEY}")

except Exception as e:
    print_message(f"FATAL ERROR starting stream: {e}")
    sys.exit(1)

# Send webhook notification
video_link = start_youtube_broadcast_stream(CAMERA_NAME)
send_webhook(CAMERA_NAME, video_link)
