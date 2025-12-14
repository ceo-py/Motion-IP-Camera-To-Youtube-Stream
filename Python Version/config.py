CAMERA_CONFIG = {
    "Kitchen": {
        "STREAM_URL": "PUT YOUR URL ON YOUR RTSP CAMERA",
        "YOUTUBE_KEY": "1234-1234-1234-1234-1234",
        "WEBHOOK_URL": "PUT YOUR URL",
        "MESSAGE":"⚠️ Motion detected by camera in Kitchen at ",
    },
    "Stairs": {
        "STREAM_URL": "PUT YOUR URL ON YOUR RTSP CAMERA",
        "YOUTUBE_KEY": "1234-1234-1234-1234-1234",
        "WEBHOOK_URL": "PUT YOUR URL",
        "MESSAGE": "⚠️ Motion detected by camera in Stairs at ",
    },
    "Yard": {
        "STREAM_URL": "PUT YOUR URL ON YOUR RTSP CAMERA",
        "YOUTUBE_KEY": "1234-1234-1234-1234-1234",
        "WEBHOOK_URL": "PUT YOUR URL",
        "MESSAGE": "⚠️ Motion detected by camera in Yard at ",
    },
}

LOG_DIR = "PATH TO LOGS/logs"
FFMPEG_BIN = "/usr/bin/ffmpeg"