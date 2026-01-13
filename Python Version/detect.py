import cv2
import os
import sys

# --- Configuration for V3 ---
# Force absolute paths to ensure the script works when called by other services
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PB_FILE = os.path.join(BASE_DIR, "models", "frozen_inference_graph.pb")
PBTXT_FILE = os.path.join(BASE_DIR, "models", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")

# --- Safety Verification ---
# This prevents the "Can't open" error by checking files before OpenCV tries to load them
if not os.path.exists(PB_FILE) or not os.path.exists(PBTXT_FILE):
    print(f"Error: Model files not found.")
    print(f"Looking for:\n - {PB_FILE}\n - {PBTXT_FILE}")
    sys.exit(1)

# Check if the PBTXT is actually valid text (not an HTML page)
if os.path.getsize(PBTXT_FILE) > 100000: # Usually ~30-40KB, HTML is >100KB
    print("Error: PBTXT file is too large. You likely downloaded the GitHub HTML page.")
    print("Please use: wget raw.githubusercontent.com")
    sys.exit(1)

# Load the model into RAM once at module level
try:
    NET = cv2.dnn.readNetFromTensorflow(PB_FILE, PBTXT_FILE)
except cv2.error as e:
    print(f"OpenCV could not load the TensorFlow model: {e}")
    sys.exit(1)

# NEW COCO IDs: 1: person, 18: dog, 17: cat
TARGETS = {1, 18, 17}

def is_target_present(rtsp_url):
    """
    Returns True if a human or animal is detected in the stream using V3 Small.
    Optimized for 2026 usage on Lenovo T410 (i5-520M).
    """
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        return False

    # 1. Skip 15 frames (1 second @ 15fps) to clear stale RTSP buffer
    # .grab() is faster as it skips decoding
    for _ in range(15):
        cap.grab()

    # 2. Capture the actual frame for AI analysis
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return False

    # 3. AI Inference
    # size=(320, 320) is the native size for MobileNet V3 Small
    # swapRB=True is required for TensorFlow models in OpenCV
    blob = cv2.dnn.blobFromImage(frame, size=(320, 320), swapRB=True, crop=False)
    NET.setInput(blob)
    detections = NET.forward()

    # 4. Process detections
    # detections.shape[2] contains the list of objects found
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > 0.55:  # Accuracy threshold
            class_id = int(detections[0, 0, i, 1])
            
            if class_id in TARGETS:
                return True
    
    return False

# Self-test logic (if run directly)
if __name__ == "__main__":
    test_url = "rtsp://admin:admin123@192.168.68.108:10554/tcp/av0_0"
    print("Testing detection...")
    if is_target_present(test_url):
        print("Target found!")
    else:
        print("No target found.")
