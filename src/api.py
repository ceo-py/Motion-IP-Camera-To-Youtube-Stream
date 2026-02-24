import os
import sys
import cv2
import datetime
from ultralytics import YOLO
from flask import Flask, jsonify, request
from utils import print_message, find_camera_key
from config import MODEL, TARGET_NAMES, TARGET_ACTIVATION, DETECT_CONF, IMAGE_SIZE, DEVICE_TYPE, TASK, CAMERA_CONFIG

# --- Model Path ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", MODEL)

if not os.path.exists(MODEL_PATH):
    sys.exit(1)

# Load model ONCE
try:
    model = YOLO(MODEL_PATH, task=TASK)
except Exception as e:
    sys.exit(f"Failed to load model: {e}")

# Create Flask app
app = Flask(__name__)

def save_picture(frame, camera_name):
    # Save image when target detected
    os.makedirs("./images", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_path = os.path.join("./images", f"{camera_name}-{timestamp}.png")
    cv2.imwrite(image_path, frame)


def is_target_present(rtsp_url: str) -> list | None:
    """
    Silent mode - no logging.
    """
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        return None

    # Clear RTSP buffer
    for _ in range(15):
        cap.grab()

    ret, frame = cap.retrieve()
    cap.release()

    if not ret:
        return None

    # 2. RUN INFERENCE
    results = model.predict(
        source=frame,
        device=DEVICE_TYPE,
        classes=list(TARGET_NAMES.keys()),
        conf=DETECT_CONF,
        imgsz=IMAGE_SIZE,
        verbose=False
    )

    target_detections = []
    camera_name = find_camera_key(rtsp_url, CAMERA_CONFIG)
    # 3. Process results silently
    for result in results:
        if len(result.boxes) == 0:
            continue

        for box in result.boxes:
            conf = float(box.conf)
            cls_id = int(box.cls)
            label = TARGET_NAMES.get(cls_id, "Unknown")
            detect_message = f"{label} ({conf:.2f})"
            print_message(f"[{camera_name}] Detected: {detect_message}")
            if cls_id not in TARGET_ACTIVATION:
                continue

            save_picture(frame, camera_name)
            target_detections.append(detect_message)

    return target_detections if target_detections else None


@app.route('/detect', methods=['GET'])
def detect_human():
    """
    API Route to detect a human in a video stream (RTSP URL).
    Example request: GET /detect?rtsp_url=rtsp://your_rtsp_url
    """
    rtsp_url = request.args.get('rtsp_url')

    if not rtsp_url:
        return jsonify({"error": "RTSP URL parameter is required."}), 400

    # Perform detection
    detection_result = is_target_present(rtsp_url)

    if detection_result:
        return jsonify({"message": detection_result}), 200
    else:
        return jsonify({"message": "No human detected."}), 200


# Run Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
