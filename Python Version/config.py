CAMERA_CONFIG = {
    "Yard": {
        "STREAM_URL": "PUT YOUR URL ON YOUR RTSP CAMERA",
        "YOUTUBE_KEY": "1234-1234-1234-1234-1234",
        "WEBHOOK_URL": "PUT YOUR URL",
        "MESSAGE": "⚠️ Motion detected by camera in Stairs at ",
    },
    "Stairs": {
        "STREAM_URL": "PUT YOUR URL ON YOUR RTSP CAMERA",
        "YOUTUBE_KEY": "1234-1234-1234-1234-1234",
        "WEBHOOK_URL": "PUT YOUR URL",
        "MESSAGE": "⚠️ Motion detected by camera in Stairs at ",
    },
    "Kitchen": {
        "STREAM_URL": "PUT YOUR URL ON YOUR RTSP CAMERA",
        "YOUTUBE_KEY": "1234-1234-1234-1234-1234",
        "WEBHOOK_URL": "PUT YOUR URL",
        "MESSAGE": "⚠️ Motion detected by camera in Stairs at ",
    },
}

YOUTUBE = {
    "SCOPES": ['https://www.googleapis.com/auth/youtube'],
    "CLIENT_SECRETS_FILE": 'client_secret.json',
    "API_SERVICE_NAME": 'youtube',
    "API_VERSION": 'v3',
    "TOKEN_FILE": 'token.json',
    "PLAYLIST_ID": 'PLV0e0d_ZUComWaSZdRi2wLH9MSYujkZvz',
}

REDIS = {
    "PORT" : "PORT NUMBER INT",
    "HOST" : "IP ADDRESS STR"
}

LOG_DIR = "PATH TO LOGS/logs"
FFMPEG_BIN = "/usr/bin/ffmpeg"
