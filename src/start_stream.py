import sys
import subprocess
from webhook import send_webhook
from utils import print_message
from youtube import start_youtube_broadcast_stream
from config import CAMERA_CONFIG, FFMPEG_BIN, INDEX_M3U8, HLS_ROOT_RAM_DISK



# --- PID Check Logic ---
# Check if ffmpeg is already running for the specific camera stream
def is_ffmpeg_streaming(CAMERA_NAME: str, YOUTUBE_KEY: str) -> bool:
    try:
        result = subprocess.run(
            ['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        for line in result.stdout.splitlines():
            if 'ffmpeg' in line and YOUTUBE_KEY in line:
                print_message(f"[{CAMERA_NAME}] Stream already running (process found).")
                return True
        return False
    except Exception as e:
        print_message(f"[{CAMERA_NAME}] Error checking ffmpeg process: {e}")
        return False


# --- Start FFmpeg Stream ---
def start_ffmpeg_stream(CAMERA_NAME, target_found):
    CAM_CONFIG = CAMERA_CONFIG[CAMERA_NAME]
    YOUTUBE_KEY = CAM_CONFIG["YOUTUBE_KEY"]

    if is_ffmpeg_streaming(CAMERA_NAME, YOUTUBE_KEY):
        return


    ffmpeg_command = [
        FFMPEG_BIN,
        '-re',                        # THROTTLE
        '-live_start_index', '-30',    # START POINT: 30 segments from the end
        '-i', f'{HLS_ROOT_RAM_DISK}/{CAMERA_NAME}/{INDEX_M3U8}',
        '-c', 'copy',
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
        print_message(f"[{CAMERA_NAME}] Successfully started YouTube stream (PID: {pid}).")
        
    except Exception as e:
        print_message(f"[{CAMERA_NAME}] FATAL ERROR starting stream: {e}")
        sys.exit(1)


    video_link = start_youtube_broadcast_stream(CAMERA_NAME)
    send_webhook(CAMERA_NAME, video_link, target_found)