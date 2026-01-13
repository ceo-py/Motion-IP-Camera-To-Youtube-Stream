import cv2
import os

# Load model ONCE at the module level to keep it in RAM
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROTO = os.path.join(BASE_DIR, "models", "deploy.prototxt")
MODEL = os.path.join(BASE_DIR, "models", "mobilenet_iter_73000.caffemodel")
NET = cv2.dnn.readNetFromCaffe(PROTO, MODEL)

# 15: person, 12: dog, 8: cat
TARGETS = {15, 12, 8}

def is_target_present(rtsp_url):
    """Returns True if a human or animal is detected in the stream."""
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        return False

    # 1. Skip 15 frames (1 second) to clear buffer
    # Use .grab() because it's faster than .read() for old CPUs
    for _ in range(15):
        cap.grab()

    # 2. NOW capture the actual frame for analysis
    ret, frame = cap.read()
    
    # 3. Release IMMEDIATELY after getting the frame
    cap.release()

    if not ret:
        return False

    # AI Inference
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    NET.setInput(blob)
    detections = NET.forward()

    # Process detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.55:
            class_id = int(detections[0, 0, i, 1])
            if class_id in TARGETS:
                return True
    
    return False
