# Motion Detection System with AI Filtering, Discord Notifications, and YouTube Streaming

This project provides a **real-time motion detection system** using a custom Python-based soft-trigger system and IP cameras. The system features **AI-driven object detection** to filter out false positives and provides direct **YouTube live links** via Discord webhooks.

No videos or snapshots are saved on the server; all processing occurs in real-time.

---

## 🚀 Features

* **Dual YOLO26 Architecture**: Uses **YOLO26n** (nano) as lightweight front-end for fast motion triggering, **YOLO26x** (large) as back-end for accurate verification.
* **OpenVINO INT8 Optimization**: Both models exported with OpenVINO INT8 quantization for 2-4x faster CPU inference - optimized for old 2-core CPUs.
* **Target Classes**: Filters for **person**, **bird**, **cat**, **dog** only (COCO classes 0, 14, 15, 16).
* **Discord notifications** with camera name, timestamp, and **direct YouTube live links**.
* **Automatic YouTube live streaming**: Initiated only when target is detected by the AI.
* **Efficient Polling**: Checks each camera every 3 seconds with minimal CPU usage.

---

# 🧠 How it Works (Logic Flow)

The system is fully Python-based and operates in a streamlined sequence:

1.  **Front-End Detection (`motion_detector.py`)**: Uses **YOLO26n** at 320p to continuously scan RTSP streams for target objects (person/bird/cat/dog). Runs every 3 seconds per camera.
2.  **Back-End Verification**: If front-end detects a target, **YOLO26x** at 640p verifies the detection with higher accuracy.
3.  **Streaming**: If back-end confirms a target, **FFmpeg** starts streaming to YouTube.
4.  **Notification**: A Discord webhook is sent with the live YouTube link.
5.  **Cleanup**: After 60 seconds of no detection, the stream stops automatically.

---

# 🛠️ Setup & Installation

### 1. Model Setup

The system uses **dual YOLO26 models** with OpenVINO INT8 optimization:

1.  **Front-End**: `yolo26n_int8_openvino_model` (nano - lightweight, fast)
2.  **Back-End**: `yolo26x_int8_openvino_model` (large - accurate)

Export your models with OpenVINO INT8 for optimal CPU performance:

```python
from ultralytics import YOLO

# Front-end model (nano, 320p)
model = YOLO("yolo26n.pt")
model.export(format="openvino", int8=True, imgsz=320)

# Back-end model (large, 640p)
model = YOLO("yolo26x.pt")
model.export(format="openvino", int8=True, imgsz=640)
```

Place both exported model folders in the `/models` subdirectory.

### 2. Dependencies

```bash
pip install -r requirements.txt
```

### 3. Google API Authentication

1.  Create a Google API project and enable **YouTube Data API**.
2.  Place `client_secret.json` in the project directory.
3.  Run `python3 generate_token.py` to create `token.json`.

---

# 🧑‍💻 Project File Structure

*   **`config.py`**: Centralized configuration for all camera URLs, keys, model paths, and settings.
*   **`motion_detector.py`**: Main monitor with dual YOLO26 model architecture (front-end + back-end).
*   **`start_stream.py`**: Initiates streaming and notifications after AI verification.
*   **`stop_stream.py`**: Gracefully terminates the streaming process and YouTube broadcast.
*   **`youtube.py`**: Integration with YouTube Data API for broadcast management.
*   **`utils.py`**: Utility functions for image processing and notifications.
*   **`webhook.py`**: Discord webhook integration.

---

# ⚙️ Running the System (Systemd Services)

To run the system reliably in the background:

### Motion Detection Service
Create `/etc/systemd/system/motion-detection.service`:

```ini
[Unit]
Description=Motion Detection with Dual YOLO26 Models
After=network.target

[Service]
User=<YOUR_USER>
WorkingDirectory=<YOUR_PROJECT_DIRECTORY>
ExecStart=<YOUR_PROJECT_DIRECTORY>/venv/bin/python3 <YOUR_PROJECT_DIRECTORY>/src/motion_detector.py
Restart=always
RestartSec=3
Environment="PATH=<YOUR_PROJECT_DIRECTORY>/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target
```

### Activation

```bash
sudo systemctl daemon-reload
sudo systemctl enable motion-detection.service
sudo systemctl start motion-detection.service
```

---

## 📅 Version History

### **v1.9.0 Latest** – Dual YOLO26 Models with OpenVINO INT8 Optimization

* **Features**:
  * **Dual Model Architecture**: Uses **YOLO26n** (nano) as lightweight front-end for motion triggering, **YOLO26x** (large) as back-end for accurate verification.
  * **OpenVINO INT8 Optimization**: Both models exported with OpenVINO INT8 quantization for 2-4x faster CPU inference - critical for old 2-core CPUs.
  * **320p Front-End**: YOLO26n runs at 320p for ultra-fast inference (~10-15ms), triggers back-end when targets (person/bird/cat/dog) detected.
  * **640p Back-End**: YOLO26x runs at 640p for accurate detection and verification.
  * **Target Classes**: Filters for person (0), bird (14), cat (15), dog (16) only.
  * **3-Second Check Interval**: Polls cameras every 3 seconds for efficient CPU usage.
  * **60-Second Cooldown**: Stream continues for 60 seconds after last detection.

---

### **[v1.8.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/b6b31a0d69a0dd65ebf936693042a8e82fd3346a)** – Switched to YOLO26X & Removed Motion Daemon
* **Features**:
  * **Upgraded to YOLO26X**: Replaced `yolo11n` with the larger, more accurate `yolo26x.onnx` model for superior detection.
  * Completely removed dependency on the `motion` daemon in favor of a custom Python soft-trigger.
  * Introduced `motion_detector.py` for efficient movement detection.
  * Optimized AI verification: Models are loaded once at startup for minimal inference delay.
  * Integrated systemd services for both the detector and the AI API.

---

### **[v1.7.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/63e30263a82133424a4f6745055ad0e4cfd035d8)** – Enhance motion detection with YOLOv4 ONNX and object verification API
* **Features**:
  * Replaced previous detection model with **YOLOv4 ONNX**.
  * Integrated local API to handle object detection.
  * Added a confidence threshold of **50%**.

---

### **[v1.6.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/753fb3cbf156b9a7f50af3309057fc197f8d21e8)** – Migrate object detection to MobileNet V3 Large
* **Features**:
  * Upgraded detection model for improved accuracy.

---

### **[v1.5.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/7344aed9e06dbc418f4f67e27df90a4a3be01dc1)** – Added AI object detection
* **Features**:
  * Integrated MobileNet-SSD version 2 for verification.

---

### **[v1.4.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/5bf5c6efccb731db457f1b98d0373f675d730154)** – Integrate YouTube broadcast with camera stream
* **Features**:
  * Automated creation and live-transition of YouTube broadcasts.

---

### **[v1.3.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/75f996df9958ca5851b45ce35d0b8ae7d46020af)** – Implement automated YouTube live stream management
* **Features**:
  * Added scheduling and automatic playlist integration.

---

### **[v1.2.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/77a5239e9b30eb6ba872b2c05875487f24e4f934)** – Major refactor of event triggering logic
* **Features**:
  * Migrated from Bash scripts to modular Python scripts and `config.py`.

---

### **[v1.1.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/71e532ef273aac2603cb364e972c57bea18a61f7)** – Added basic motion detection and alerting
* **Features**:
  * Initial implementation with basic alerts and no AI filtering.

---
