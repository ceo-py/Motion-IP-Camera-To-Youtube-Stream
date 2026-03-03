CAMERA_CONFIG = {
    "Balcony": {
        "STREAM_URL": "RTSP URL",
        "YOUTUBE_KEY": "STREAMING KEY",
        "WEBHOOK_URL": "DISCORD WEB HOOK URL",
        "MESSAGE":"⚠️ Motion detected by camera on Balcony at"},
    "Stairs": {
        "STREAM_URL": "RTSP URL",
        "YOUTUBE_KEY": "STREAMING KEY",
        "WEBHOOK_URL": "DISCORD WEB HOOK URL",
        "MESSAGE": "⚠️ Motion detected by camera on Stairs at"},
    "Kitchen": {
        "STREAM_URL": "RTSP URL",
        "YOUTUBE_KEY": "STREAMING KEY",
        "WEBHOOK_URL": "DISCORD WEB HOOK URL",
        "MESSAGE": "⚠️ Motion detetion by camera on Kitchen at"},
}

YOUTUBE = {
    "SCOPES": ['https://www.googleapis.com/auth/youtube'],
    "CLIENT_SECRETS_FILE": 'PATH JSON',
    "API_SERVICE_NAME": 'youtube',
    "API_VERSION": 'v3',
    "TOKEN_FILE": 'PATH TOKEN JSON',
    "PLAYLIST_ID": 'PLAYLIST ID',
    "VIDEO_URL": 'https://www.youtube.com/watch?v=',
    "THUMBNAIL_PATH": 'PATH TO SAVE TMN',
}

REDIS = {
    "PORT" : 6379,
    "HOST" : "localhost"
}

LOG_DIR = "PATH"
FFMPEG_BIN = "PATH"
HLS_ROOT_RAM_DISK="PATH"
INDEX_M3U8="index.m3u8"


# API CONFIGURATION
MODEL = "yolo26x_int8_openvino_model"
DETECT_CONF = 0.50
FRONT_MODEL = "yolo26s_int8_openvino_model"
BACK_MODEL = "yolo26x_int8_openvino_model"
TARGET_ACTIVATION = [0, 14, 15, 16]
BACK_DETECT_CONF = 0.50
FRONT_DETECT_CONF = 0.30  # Higher for 320p to reduce false positives
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
    "THRESHOLD": 200,           # Frame diff: 200 pixels (very sensitive for static cameras)
    "SENSITIVITY": 15,          # Pixel intensity delta (0-255) (was 20)
    "DOWNSCALE_WIDTH": 320,
    "FORCE_RESIZE": False,
    "CHECK_INTERVAL": 0.8,      # Slightly faster polling for windows
    "MIN_MOTION_FRAMES": 4,     # Need 4 consecutive motion frames
    "COOLDOWN_PERIOD": 60,      # Wait longer before stopping stream
    "LEARNING_RATE": 0.05,      # How fast the background model adapts (0.01 - 0.1)
    "KNN_WARMUP_FRAMES": 30,   # Frames to skip while KNN learns background
}