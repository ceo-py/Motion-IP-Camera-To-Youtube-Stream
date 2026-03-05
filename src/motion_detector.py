import cv2
import time
import os
from ultralytics import YOLO
from concurrent.futures import ThreadPoolExecutor
from config import CAMERA_CONFIG, MOTION_DETECTION, FRONT_MODEL, BACK_MODEL, FRONT_DETECT_CONF, BACK_DETECT_CONF, IMAGE_SIZE, TARGET_ACTIVATION, DEVICE_TYPE, TARGET_NAMES, HLS_ROOT_RAM_DISK, INDEX_M3U8
from utils import print_message, save_picture, draw_detect_objectcv
from start_stream import start_ffmpeg_stream
from stop_stream import stop_ffmpeg_stream

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONT_MODEL_PATH = os.path.join(BASE_DIR, "models", FRONT_MODEL)
BACK_MODEL_PATH = os.path.join(BASE_DIR, "models", BACK_MODEL)
CHECK_INTERVAL = 3  # Seconds between AI checks per camera

class YOLO26Gatekeeper:
    """A shared AI engine to prevent loading the model multiple times."""
    def __init__(self, front_model_path, back_model_path):
        # Load the OpenVINO model specifically for Intel CPU
        self.front_model = YOLO(front_model_path, task='detect')
        self.back_model = YOLO(back_model_path, task='detect')

    def front_has_targets(self, frame, camera_name):
        if frame is None: return False

        results = self.front_model.predict(
            source=frame,
            imgsz='320',
            classes=TARGET_ACTIVATION,
            conf=FRONT_DETECT_CONF,
            verbose=False,
            device=DEVICE_TYPE
        )

        correct_targets = []
        for result in results:
            if len(result.boxes) == 0:
                continue

            for box in result.boxes:
                conf = float(box.conf)
                cls_id = int(box.cls)
                label = TARGET_NAMES.get(cls_id, "Unknown")
                detect_message = f"{label} ({conf:.2f})"
                print_message(f"[{camera_name}] Front Detected: {detect_message}")
                correct_targets.append(detect_message)

        return len(correct_targets) > 0

    def back_has_targets(self, frame, camera_name):
        results = self.back_model.predict(
        source=frame,
        device=DEVICE_TYPE,
        classes=list(TARGET_NAMES.keys()),
        conf=BACK_DETECT_CONF,
        imgsz=IMAGE_SIZE,
        verbose=False
    )

        target_detections = []

        # 3. Process results silently
        for result in results:
            if len(result.boxes) == 0:
                continue

            for box in result.boxes:
                conf = float(box.conf)
                cls_id = int(box.cls)
                label = TARGET_NAMES.get(cls_id, "Unknown")
                detect_message = f"{label} ({conf:.2f})"
                print_message(f"[{camera_name}] Back Detected: {detect_message}")

                if cls_id not in TARGET_ACTIVATION:
                    continue
                frame_with_box = draw_detect_objectcv(cv2, box, frame, label, conf)
                save_picture(cv2, frame_with_box, camera_name)
                target_detections.append(detect_message)

        return target_detections if target_detections else None



class CameraWorker:
    # When streaming: use HLS to detect stop (matches delayed content)
    # When NOT streaming: use RTSP to detect start (real-time)
    def __init__(self, camera_name, stream_url, hls_url, gatekeeper):
        self.camera_name = camera_name
        self.hls_url = hls_url
        self.stream_url = stream_url[:-1] + "1"
        self.gatekeeper = gatekeeper
        self.last_check_time = 0
        self.is_streaming = False
        self.stream_start_time = 0
        self.last_reconnect_time = 0


    def get_fresh_frame(self):
        # When streaming: use HLS buffer (delayed, matches what's being streamed)
        # When NOT streaming: use RTSP (real-time)
        url = self.hls_url if self.is_streaming else self.stream_url
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            return None
        for _ in range(5):
            cap.grab()
        ret, frame = cap.read()
        cap.release()
        return frame if ret else None


    def run_cycle(self):
        current_time = time.time()

        if self.is_streaming and current_time - self.stream_start_time < MOTION_DETECTION.get('COOLDOWN_PERIOD', 60):
            return

        if current_time - self.last_check_time < CHECK_INTERVAL:
            return

        frame = self.get_fresh_frame()
        if frame is None: return

        # Perform the "Front-End" AI Check
        is_targets = self.gatekeeper.front_has_targets(frame, self.camera_name)
        self.last_check_time = current_time


        if is_targets and not self.is_streaming:
            target_found = self.gatekeeper.back_has_targets(frame, self.camera_name)
            if not target_found:
                return
            start_ffmpeg_stream(self.camera_name, target_found)
            self.is_streaming = True
            self.stream_start_time = time.time()

        elif self.is_streaming and not is_targets:
            self.is_streaming = False
            self.stream_start_time = 0
            stop_ffmpeg_stream(self.camera_name)


def main():
    # 1. Initialize the SHARED model once
    gatekeeper = YOLO26Gatekeeper(FRONT_MODEL_PATH, BACK_MODEL_PATH)
    # 2. Setup your cameras (Load from your CAMERA_CONFIG)
    # Example: cameras = [CameraWorker("FrontDoor", "rtsp://...", gatekeeper), ...]
    cameras = []
    for name, cfg in CAMERA_CONFIG.items():
        hls_url = f"{HLS_ROOT_RAM_DISK}/{name}/{INDEX_M3U8}"
        cameras.append(CameraWorker(name, cfg["STREAM_URL"], hls_url, gatekeeper))

    print(f"Monitoring {len(cameras)} cameras every {CHECK_INTERVAL}s...")

    # 3. Main Loop
    with ThreadPoolExecutor(max_workers=len(cameras)) as executor:
        while True:
            futures = [executor.submit(cam.run_cycle) for cam in cameras]
            for f in futures:
                f.result()
            time.sleep(0.1) # Prevents 100% CPU usage on the main thread

if __name__ == "__main__":
    main()