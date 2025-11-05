#!/bin/bash

# Start YouTube live stream from IP camera (Kitchen) safely

CAMERA_NAME="Kitchen"
STREAM_URL="PATH TO YOUR RTSP"
YOUTUBE_KEY="1234-1234-1234-1234-1234"

LOG_DIR="PATH TO LOG DIRECTORY"
LOG_FILE="${LOG_DIR}/ffmpeg-${CAMERA_NAME}.log"
PID_FILE="${LOG_DIR}/ffmpeg-${CAMERA_NAME}.pid"

# Ensure log directory exists and is writable
mkdir -p "$LOG_DIR"
chmod 775 "$LOG_DIR"

# Check if stream is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "$(date) - Stream already running for $CAMERA_NAME (PID: $PID)" >> "$LOG_FILE"
        exit 0
    else
        echo "$(date) - Stale PID file found, removing..." >> "$LOG_FILE"
        rm -f "$PID_FILE"
    fi
fi

# Start FFmpeg stream in the background
nohup /usr/bin/ffmpeg -rtsp_transport tcp -i "$STREAM_URL" \
    -c copy -f flv "rtmp://a.rtmp.youtube.com/live2/$YOUTUBE_KEY" \
    > "$LOG_FILE" 2>&1 &

# Save process ID
echo $! > "$PID_FILE"

echo "$(date) - Started YouTube stream for $CAMERA_NAME (PID: $(cat "$PID_FILE"))" >> "$LOG_FILE"

# Send Message to Discord

PATH TO WEBHOOK SCRIPT/webhook-ipcamera-kitchen.sh ipcamera-kitchen