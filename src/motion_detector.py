import cv2
import time
from config import CAMERA_CONFIG, MOTION_DETECTION
from utils import print_message
from concurrent.futures import ThreadPoolExecutor
from detect import is_target_present
from start_stream import start_ffmpeg_stream
from stop_stream import stop_ffmpeg_stream



class MotionDetector:
    def __init__(self, camera_name, stream_url):
        self.camera_name = camera_name
        self.stream_url = stream_url
        self.motion_stream_url = stream_url

        print_message(f"[{self.camera_name}] Primary stream: {self.stream_url}")
        print_message(f"[{self.camera_name}] Motion check stream: {self.motion_stream_url}")

        self.avg = None
        self.motion_counter = 0
        self.last_motion_time = 0
        self.was_moving = False

    def get_frame(self):
        cap = cv2.VideoCapture(self.motion_stream_url)
        if not cap.isOpened():
            return None
        for _ in range(5):
            cap.grab()
        ret, frame = cap.read()
        cap.release()
        return frame if ret else None

    def process_frame(self, frame):
        if frame is None:
            return False

        # Resize only if forced or if frame is larger than 640
        process_frame = frame
        if MOTION_DETECTION.get("FORCE_RESIZE", False) or frame.shape[1] > 640:
            width = MOTION_DETECTION.get("DOWNSCALE_WIDTH", 320)
            height = int(frame.shape[0] * (width / frame.shape[1]))
            process_frame = cv2.resize(frame, (width, height))

        gray = cv2.cvtColor(process_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.avg is None:
            self.avg = gray.copy().astype("float")
            return False

        # Parameters for window recording
        learning_rate = MOTION_DETECTION.get("LEARNING_RATE", 0.05)
        sensitivity = MOTION_DETECTION.get("SENSITIVITY", 20)

        # Compute difference from moving average
        cv2.accumulateWeighted(gray, self.avg, learning_rate)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
        thresh = cv2.threshold(frameDelta, sensitivity, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for c in cnts:
            if cv2.contourArea(c) < MOTION_DETECTION.get("THRESHOLD", 600):
                print_message(f"[{self.camera_name}] Nothing Found!!")
                continue
            motion_detected = True
            break

        return motion_detected

    def check_motion(self):
        frame = self.get_frame()
        motion_detected = self.process_frame(frame)

        if motion_detected:
            self.motion_counter +=1

        elif not motion_detected and self.motion_counter != 0:
            self.motion_counter = 0


        if not self.was_moving and self.motion_counter > MOTION_DETECTION.get("MIN_MOTION_FRAMES", 4):
            print_message(f"[{self.camera_name}] Threshold reached. Triggering AI detection...")
            self.stream_process()

        elif self.was_moving and (time.time() - self.last_motion_time) < 60:
            return

        elif self.was_moving and (time.time() - self.last_motion_time > MOTION_DETECTION.get("COOLDOWN_PERIOD", 15)):
            self.stream_process()



    def stream_process(self):
        self.last_motion_time = time.time()
        target_found = is_target_present(self.stream_url)

        if not target_found:
            print_message(f"[{self.camera_name}] No Human/Animal Detected!!")

            if self.was_moving:
                stop_ffmpeg_stream(self.camera_name)
                self.was_moving = False

        elif target_found and not self.was_moving:
            start_ffmpeg_stream(self.camera_name, target_found)
            print_message(f"[{self.camera_name}] AI Detected {target_found}!!")
            self.was_moving = True



def main():
    detectors = []
    for cam_name, config in CAMERA_CONFIG.items():
        detectors.append(MotionDetector(cam_name, config["STREAM_URL"]))

    print_message(f"Starting window-optimized motion detection for {len(detectors)} cameras...")
    with ThreadPoolExecutor() as executor:
        while True:
            # Submit tasks to executor for each detector (camera)
            futures = [executor.submit(detector.check_motion) for detector in detectors]

            # Wait for all threads to complete
            for future in futures:
                future.result()  # Blocks until the result is available

            # Sleep between iterations
            time.sleep(MOTION_DETECTION.get("CHECK_INTERVAL", 0.8))


if __name__ == "__main__":
    main()