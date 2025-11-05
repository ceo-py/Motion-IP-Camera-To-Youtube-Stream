#!/bin/bash
# Stop YouTube live stream for IP camera (Kitchen)

CAMERA_NAME="Kitchen"
LOG_DIR="/home/ceo/production/logs"
LOG_FILE="${LOG_DIR}/ffmpeg-${CAMERA_NAME}.log"
PID_FILE="${LOG_DIR}/ffmpeg-${CAMERA_NAME}.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "$(date) - Stopping FFmpeg for $CAMERA_NAME (PID: $PID)" >> "$LOG_FILE"
        kill "$PID"
        sleep 3
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "$(date) - Force killing FFmpeg (PID: $PID)" >> "$LOG_FILE"
            kill -9 "$PID"
        fi
    else
        echo "$(date) - PID $PID not active, removing stale PID file" >> "$LOG_FILE"
    fi
    rm -f "$PID_FILE"
else
    echo "$(date) - No PID file found for $CAMERA_NAME" >> "$LOG_FILE"
fi