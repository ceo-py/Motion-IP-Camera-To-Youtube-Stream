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
    "PLAYLIST_ID": 'ID PLAYLIST STR',
    "VIDEO_URL": 'https://www.youtube.com/watch?v=',
}

REDIS = {
    "PORT" : "PORT NUMBER INT",
    "HOST" : "IP ADDRESS STR"
}

LOG_DIR = "PATH TO LOGS/logs"
FFMPEG_BIN = "/usr/bin/ffmpeg"

# API CONFIGURATION
MODEL = "yolo26x.onnx"
TARGET_ACTIVATION = [0, 14, 15, 16]
DETECT_CONF = 0.50
IMAGE_SIZE = 640
DEVICE_TYPE = 'cpu'
TARGET_NAMES = {
    0: "person", 1: "bicycle", 2: "car", 3: "motorbike", 4: "aeroplane", 5: "bus",
    6: "train", 7: "truck", 8: "boat", 9: "traffic light", 10: "fire hydrant",
    11: "stop sign", 12: "parking meter", 13: "bench", 14: "bird", 15: "cat",
    16: "dog", 17: "horse", 18: "sheep", 19: "cow", 20: "elephant", 21: "bear",
    22: "zebra", 23: "giraffe", 24: "backpack", 25: "umbrella", 26: "handbag",
    27: "tie", 28: "suitcase", 29: "frisbee", 30: "skis", 31: "snowboard",
    32: "sports ball", 33: "kite", 34: "baseball bat", 35: "baseball glove",
    36: "skateboard", 37: "surfboard", 38: "tennis racket", 39: "bottle", 40: "wine glass",
    41: "cup", 42: "fork", 43: "knife", 44: "spoon", 45: "bowl", 46: "banana",
    47: "apple", 48: "sandwich", 49: "orange", 50: "broccoli", 51: "carrot",
    52: "hot dog", 53: "pizza", 54: "donut", 55: "cake", 56: "chair", 57: "couch",
    58: "potted plant", 59: "bed", 60: "dining table", 61: "toilet", 62: "tv",
    63: "laptop", 64: "mouse", 65: "remote", 66: "keyboard", 67: "cell phone",
    68: "microwave", 69: "oven", 70: "toaster", 71: "sink", 72: "refrigerator",
    73: "book", 74: "clock", 75: "vase", 76: "scissors", 77: "teddy bear",
    78: "hair drier", 79: "toothbrush"
}
TASK = "detect"
DETECT_ENDPOINT = "http://127.0.0.1:8001/detect?rtsp_url="

# MOTION DETECTION CONFIGURATION
# Optimized for 2-core CPU & Window recording
MOTION_DETECTION = {
    "THRESHOLD": 250,           # Catch smaller objects (like cats in distance)
    "SENSITIVITY": 15,          # Pick up lower contrast through glass
    "DOWNSCALE_WIDTH": 320,
    "FORCE_RESIZE": False,
    "CHECK_INTERVAL": 0.8,
    "MIN_MOTION_FRAMES": 3,     # Trigger slightly faster
    "COOLDOWN_PERIOD": 15,
    "LEARNING_RATE": 0.05,
}