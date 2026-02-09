# Motion Detection System with AI Filtering, Discord Notifications, and YouTube Streaming

This project provides a **real-time motion detection system** using a custom Python-based soft-trigger system and IP cameras. The system features **AI-driven object detection** to filter out false positives and provides direct **YouTube live links** via Discord webhooks.

No videos or snapshots are saved on the server; all processing occurs in real-time.

---

## 🚀 Features

* **Custom Motion Soft-Trigger**: Uses a dedicated Python script (`motion_detector.py`) to monitor RTSP streams for movement, replacing the legacy `motion` daemon.
* **AI Filtering (YOLOv4 with ONNX)**: Uses **YOLOv4 ONNX** model (`yolo11n.onnx`) for object detection. It checks if motion is caused by a **human** (default target for alerts) or a **dog**/ **cat**.
* **Discord notifications** with camera name, timestamp, and **direct YouTube live links**.
* **Automatic YouTube live streaming**: Initiated only when a **human** is detected by the AI.
* **Optimized for Performance**: The AI model is loaded into memory once by a local API, ensuring rapid verification without reloading the model for every trigger.

---

# 🧠 How it Works (Logic Flow)

The system is fully Python-based and operates in a streamlined sequence:

1.  **Detection (`motion_detector.py`)**: Continuously monitors low-resolution RTSP streams for pixel changes. This acts as a "soft trigger" to minimize resource usage.
2.  **Trigger (`start-stream.py`)**: When significant motion is detected, `motion_detector.py` triggers this script.
3.  **AI Verification (`detect.py` & `api.py`)**: `start-stream.py` calls the local AI API.
    *   **Crucial**: `api.py` loads the YOLOv4 model into RAM on startup. Subsequent calls for detection are nearly instantaneous because the model is **already in memory**.
4.  **Streaming**: If the AI confirms a **human**, an FFmpeg process is started to stream the high-resolution feed to YouTube.
5.  **Notification**: A Discord webhook is sent with the live YouTube link.
6.  **Cleanup (`stop-stream.py`)**: After the motion stops and a cooldown period expires, the detector calls this script to terminate the stream and close the broadcast.

---

# 🛠️ Setup & Installation

### 1. Model Setup

Place the `yolo11n.onnx` file in the `/models` subdirectory.

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

*   **`config.py`**: Centralized configuration for all camera URLs, keys, and settings.
*   **`motion_detector.py`**: The main monitor that uses OpenCV for movement detection.
*   **`api.py`**: The Flask/Gunicorn-based API that keeps the YOLO model resident in memory.
*   **`start-stream.py`**: Initiates streaming and notifications after AI verification.
*   **`stop-stream.py`**: Gracefully terminates the FFmpeg process and YouTube broadcast.
*   **`detect.py`**: Client-side logic for calling the AI API.
*   **`youtube.py`**: Integration with YouTube Data API for broadcast management.
*   **`redis_utils.py`**: Persistence layer for tracking active stream states.

---

# ⚙️ Running the System (Systemd Services)

To run the system reliably in the background:

### 1. Object Detection API Service
Create `/etc/systemd/system/ip-camera-api.service`:

```ini
[Unit]
Description=Gunicorn instance for ip-camera detection API
After=network.target

[Service]
User=<YOUR_USER>
Group=www-data
WorkingDirectory=<YOUR_PROJECT_DIRECTORY>
ExecStart=/bin/bash -c 'source venv/bin/activate && exec gunicorn --workers 1 --bind 127.0.0.1:8001 api:app'
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. Motion Detection Automate System Service
Create `/etc/systemd/system/motion-detection.service`:

```ini
[Unit]
Description=Motion Detection Automate System
After=network.target

[Service]
User=<YOUR_USER>
WorkingDirectory=<YOUR_PROJECT_DIRECTORY>
ExecStart=<YOUR_PROJECT_DIRECTORY>/venv/bin/python3 <YOUR_PROJECT_DIRECTORY>/motion_detector.py
Restart=always
RestartSec=3
Environment="PATH=<YOUR_PROJECT_DIRECTORY>/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target
```

### 3. Activation

```bash
sudo systemctl daemon-reload
sudo systemctl enable ip-camera-api.service motion-detection.service
sudo systemctl start ip-camera-api.service motion-detection.service
```

---

## 📅 Version History

### **v1.8.0 Latest** – Removed Motion Daemon, added Custom Python Soft-Trigger
* **Features**:
  * Completely removed dependency on the `motion` daemon.
  * Introduced `motion_detector.py` for efficient movement detection.
  * Optimized AI verification: The model is now kept resident in memory via `api.py` to prevent reload delays.
  * Integrated systemd services for both the detector and the AI API.

---

### **v1.7.0** – Enhance motion detection with YOLOv4 ONNX and object verification API
* **Features**:
  * Replaced previous detection model with **YOLOv4 ONNX** (`yolo11n.onnx`).
  * Integrated local API to handle object detection.
  * Added a confidence threshold of **50%**.

---

### **[v1.6.0]** – Migrate object detection to MobileNet V3 Large
* **Features**:
  * Upgraded detection model for improved accuracy.

---

### **[v1.5.0]** – Added AI object detection
* **Features**:
  * Integrated MobileNet-SSD version 2 for verification.

---

### **[v1.4.0]** – Integrate YouTube broadcast with camera stream
* **Features**:
  * Automated creation and live-transition of YouTube broadcasts.

---

### **[v1.3.0]** – Implement automated YouTube live stream management
* **Features**:
  * Added scheduling and automatic playlist integration.

---

### **[v1.2.0]** – Major refactor of event triggering logic
* **Features**:
  * Migrated from Bash scripts to modular Python scripts and `config.py`.

---

### **[v1.1.0]** – Added basic motion detection and alerting
* **Features**:
  * Initial implementation with basic alerts and no AI filtering.

---
