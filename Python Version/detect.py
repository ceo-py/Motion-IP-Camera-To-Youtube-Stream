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

# Load the model into RAM once at module level
try:
    NET = cv2.dnn.readNetFromTensorflow(PB_FILE, PBTXT_FILE)
except cv2.error as e:
    print(f"OpenCV could not load the TensorFlow model: {e}")
    sys.exit(1)

# NEW COCO IDs: 1: person, 18: dog, 17: cat
TARGETS = {1: "Human", 18: "Dog", 17: "Cat"}
COCO_CLASSES = {
    1: "person",
    2: "bicycle",
    3: "car",
    4: "motorbike",
    5: "aeroplane",
    6: "bus",
    7: "train",
    8: "truck",
    9: "boat",
    10: "traffic light",
    11: "fire hydrant",
    13: "dog",
    14: "horse",
    15: "sheep",
    16: "cow",
    17: "cat",
    18: "dog",
    19: "horse",
    20: "sheep",
    21: "cow",
    22: "cat",
    23: "dog",
    24: "horse",
    25: "sheep",
    26: "cow",
    27: "cat",
    28: "dog",
    29: "horse",
    30: "sheep",
    31: "cow",
    32: "dog",
    33: "horse",
    34: "sheep",
    35: "cow",
    36: "cat",
    37: "dog",
    38: "horse",
    39: "sheep",
    40: "cow",
    41: "cat",
    42: "dog",
    43: "horse",
    44: "sheep",
    45: "cow",
    46: "cat",
    47: "dog",
    48: "horse",
    49: "sheep",
    50: "cow"
}



def is_target_present(rtsp_url):
    """
    Returns True if a human or animal is detected in the stream using V3 Small.
    Optimized for 2026 usage on Lenovo T410 (i5-520M).
    """
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        return 

    # 1. Skip 15 frames (1 second @ 15fps) to clear stale RTSP buffer
    # .grab() is faster as it skips decoding
    for _ in range(15):
        cap.grab()

    # 2. Capture the actual frame for AI analysis
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return 

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

        if confidence > 0.75:  # Accuracy threshold
            class_id = int(detections[0, 0, i, 1])

            if class_id in TARGETS:
                found = f"Detected: {COCO_CLASSES.get('class_id')} with confidence: {confidence:.2f}!"
                return found

    return 

# Self-test logic (if run directly)
if __name__ == "__main__":
    test_url = "rtsp://your_test_stream_here"
    print("Testing detection...")
    if is_target_present(test_url):
        print("Target found!")
    else:
        print("No target found.")