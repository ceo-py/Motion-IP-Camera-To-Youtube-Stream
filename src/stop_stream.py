# stop_stream.py
import os
import signal
import time
from utils import print_message
from youtube import go_end_stream
from config import CAMERA_CONFIG
import subprocess



def is_ffmpeg_streaming(CAMERA_NAME:str, pid: int) -> None:
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


def stop_ffmpeg_stream(CAMERA_NAME: str) -> None:
    CAM_CONFIG = CAMERA_CONFIG[CAMERA_NAME]
    YOUTUBE_KEY = CAM_CONFIG["YOUTUBE_KEY"]

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
                is_ffmpeg_streaming(CAMERA_NAME, pid)
                return
            
        print_message(f"[{CAMERA_NAME}] No active stream is found.")
    except Exception as e:
        print(f"[{CAMERA_NAME}] Error checking ffmpeg process: {e}")
