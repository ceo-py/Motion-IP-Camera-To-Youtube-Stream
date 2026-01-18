# Motion Detection System with AI Filtering, Discord Notifications, and YouTube Streaming

This project provides a **real-time motion detection system** using the [Motion](motion-project.github.io) daemon and IP cameras. The system features **AI-driven object detection** to filter out false positives and provides direct **YouTube live links** via Discord webhooks.

No videos or snapshots are saved on the server; all processing occurs in real-time.

---

## 🚀 Features

* **AI Filtering (YOLOv4 with ONNX)**: Uses **YOLOv4 ONNX** model (`yolo11n.onnx`) for object detection. It checks if motion is caused by a **human** (default target for alerts) or a **dog**/ **cat**.
* **Real-time motion detection** from multiple IP cameras.
* **Discord notifications** with camera name, timestamp, and **direct YouTube live links**.
* **Automatic YouTube live streaming** is initiated only when a **human** is detected by the AI.
* **Optimized for Low CPU Usage**: Specifically tuned for low CPU usage on older hardware (e.g., 2010+ CPUs).

---

# 🧠 AI Detection & Filtering (YOLOv4 ONNX)

To reduce false alarms caused by wind, shadows, or cars, the system utilizes the **YOLOv4 ONNX** model to detect **humans, cats, and dogs**. This helps ensure that only valid motion events trigger alerts and YouTube streaming.

### Model Setup

Place the following files in the `/models` subdirectory relative to your scripts:

* `yolo11n.onnx` (YOLOv4 ONNX weights)

### Logic:

When **Motion** triggers an event, the `detect.py` script:

1. Clears the stale RTSP buffer (skipping 15 frames).
2. Analyzes the live frame using the YOLO model.
3. If a **human** (ID: 0), **dog** (ID: 16), or **cat** (ID: 15) is detected with greater than 50% confidence, it triggers an alert. If no valid object is detected, the script exits early to save CPU usage.

### AI Dependencies

## 1. Installation Guide (Python)

```bash
pip install -r requirements.txt
```

---

# 📡 API Integration for Object Detection

The motion detection system has been updated to use a **local API** for object detection, improving accuracy and reducing resource load. The **AI model** (YOLOv4 ONNX) is now loaded **once** on startup and the detection is handled inside the API, reducing redundant processing.

### API Setup:

1. The **API** checks for the presence of human-like objects when motion is detected.
2. The API is called to verify if **human, dog, or cat** is detected.
3. Only **human detection** triggers the live stream and sends Discord notifications with the YouTube stream link.

### API Endpoint:

* **GET** `/detect?rtsp_url=<rtsp_url>`: Sends a request to check the RTSP stream for object detection.

---

## 🧑‍💻 Method 1: Python System (Recommended for Scalability) 🐍

This method uses **centralized configuration** (`config.py`) and **modular Python scripts** (`start_stream.py`, `send_webhook.py`) for easy maintenance and management of multiple cameras.

### Project File Structure

Place the following Python scripts and configuration file in a dedicated directory (e.g., `/PATH/TO/YOUR/SCRIPTS`):

1. **`config.py`**: Centralized configuration for all camera-specific URLs, keys, and webhook addresses.
2. **`start_stream.py`**: Starts the YouTube live stream using **FFmpeg** and sends a webhook notification.
3. **`stop_stream.py`**: Stops the live stream and sends a webhook.
4. **`send_webhook.py`**: Reusable function to send motion-triggered alerts to Discord.
5. **`api.py`**: The API that loads the YOLOv4 ONNX model and handles incoming requests to check for objects in the RTSP stream. This API ensures that the model is loaded into memory once, avoiding redundant loads on each call.
6. **`generate_token.py`**: This script is used to authenticate with the YouTube API by generating a `token.json` file. The token allows the system to interact with YouTube, including starting and stopping streams. The token may expire, and this script allows you to regenerate it when needed.
7. **`redis_utils.py`**: Utility script for interacting with Redis. It helps track which cameras are currently running, allowing the system to start and stop them based on motion detection events. This ensures that only the necessary streams are active.
8. **`youtube.py`**: Contains the logic for interacting with the YouTube API, including starting a live stream, saving videos to a playlist, stopping the stream, and managing all other aspects of YouTube streaming and broadcasting.
9. **`utils.py`**: Provides helper functions for formatting and sending messages. This script includes functions for adding timestamps and other relevant information to the notifications that are sent via Discord.


### Permissions (MANDATORY)

Since **Motion** runs as the **root** user via `systemd`, you must ensure the following are configured correctly:

| **Target**           | **Requirement**                       | **Command**                                |
| :------------------- | :------------------------------------ | :----------------------------------------- |
| **Scripts** (`*.py`) | **Execute** permission & Shebang line | `chmod +x *.py`                            |
| **Log Directory**    | Directory must exist                  | `sudo mkdir -p /PATH/TO/YOUR/SCRIPTS/logs` |

Make sure the **first line** of `start_stream.py`, `stop_stream.py`, and `send_webhook.py` is:

```python
#!/usr/bin/env python3
```

## 2. Configuration (`config.py`)

The configuration file includes camera-specific settings like stream URLs, YouTube keys, and Discord webhook URLs. For example:

```python
# config.py

LOG_DIR = "/PATH/TO/YOUR/SCRIPTS/logs"
FFMPEG_BIN = "/usr/bin/ffmpeg"

CAMERA_CONFIG = {
    "Kitchen": {
        "STREAM_URL": "rtsp://...",
        "YOUTUBE_KEY": "1234-1234-1234-1234-1234",
        "CHAT_INFO": "Kitchen Live Stream",
        "WEBHOOK_URL": "https://discord.com/api/webhooks/xxxx",
        "MESSAGE": "🚨 Motion Alert: Kitchen Camera at"
    },
    # Add other cameras...
}
```

## 3. Motion Configuration Integration (Python)

Update the Motion configuration for each camera (e.g., `/etc/motion/ipcamera-kitchen.conf`) to trigger the appropriate Python scripts when motion is detected.

```conf
############################################################
# Event Handling - Python Scripts
############################################################

# Start the stream when motion is detected (calls start_stream.py and sends "LIVE" webhook)
on_event_start /usr/bin/python3 /path/to/your/scripts/start_stream.py Kitchen

# Stop the stream when motion ends
on_event_end /usr/bin/python3 /path/to/your/scripts/stop_stream.py Kitchen
```

## 📝 Notes

* **Tuning:** Adjust `threshold` and `minimum_motion_frames` in Motion’s config file for correct motion sensitivity.
* **Testing:** Use `emulate_motion on` in your camera config for testing automation and verifying that triggers are firing correctly.

---

# 🧩 Running the System (Both Methods)

1. **Start or restart Motion** to apply the new configuration:

   ```bash
   sudo systemctl enable motion
   sudo systemctl restart motion
   sudo systemctl status motion
   ```

## 🔑 Google API Authentication (`token.json`)

To interact with YouTube's API for live streaming, authenticate with Google and generate the `token.json` file. Follow these steps:

1. **Create a Google API project** and enable the **YouTube Data API**.

2. **Download OAuth 2.0 credentials** and place the `client_secret.json` file in your project directory.

3. **Generate the `token.json` file** by running the authentication script:

   ```bash
   python3 generate_token.py
   ```

4. **Use `token.json` for Authentication** in the Python scripts (`start_stream.py`, `stop_stream.py`) to authenticate and interact with YouTube’s API.


### **Updated AI Integration:**

The object detection part of the system is now handled via a **local API** that checks if the detected motion corresponds to a **human, cat, or dog** using YOLOv4 (`yolo11n.onnx`). This reduces CPU usage and improves the accuracy of alerts. The **AI API** is only called when motion is detected, and only if a **human** is confirmed by the AI does the system proceed to send alerts and start streaming.

---

## 🛠️ **Setting up the API as a Service (with Gunicorn)**

To run the object detection API in a persistent and reliable way, we use **Gunicorn** to serve the API and **systemd** to manage it as a service.

### API Service Setup:

1. **Create a systemd service file** for your API:

```ini
[Unit]
Description=Gunicorn instance for ip-camera
After=network.target

[Service]
User=<YOUR_USER>
Group=www-data
WorkingDirectory=<YOUR_PROJECT_DIRECTORY>
# Activate virtual environment and start Gunicorn
ExecStart=/bin/bash -c 'source <YOUR_PROJECT_DIRECTORY>/venv/bin/activate && exec gunicorn --workers 1 --bind 127.0.0.1:8001 api:app'
Restart=always

[Install]
WantedBy=multi-user.target
```

* Replace `<YOUR_USER>` with the user under which you want to run the service.
* Replace `<YOUR_PROJECT_DIRECTORY>` with the path to your project directory.

2. **Place the service file** in `/etc/systemd/system/` with a name like `ip-camera-api.service`.

3. **Enable and start the service**:

```bash
sudo systemctl enable ip-camera-api.service
sudo systemctl start ip-camera-api.service
```

4. **Check service status**:

```bash
sudo systemctl status ip-camera-api.service
```


Sure! Here's the **Version History** section styled in the format suitable for a `README.md` file, with the latest changes at the top:

---

## 📅 Version History

### **v1.7.0 Latest** – Enhance motion detection with YOLOv4 ONNX and object verification API

* **Features**:

  * Replaced previous detection model with **YOLOv4 ONNX** (`yolo11n.onnx`) for more accurate object detection.
  * Integrated a new **local API** to handle object detection and filter motion events based on AI results (human, dog, cat).
  * Streamlined detection process to reduce CPU usage by calling the AI model only when motion is detected.
  * Added a confidence threshold of **50%** to ensure that only valid detections trigger actions (e.g., YouTube streaming, Discord alerts).

**Key Changes**:

* Replaced `detect.py` logic to integrate YOLOv4 ONNX for object detection via an API.
* Refactored object detection flow to improve accuracy and reduce false alarms (especially from wind, shadows, or cars).
* Updated Motion configuration to call the new API, ensuring AI checks before triggering alerts.
* Enhanced webhook notification to include the detected object type and confidence level before initiating the stream.
* Optimized CPU performance by skipping stale frames and minimizing redundant processing.

---

### **[v1.6.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/753fb3cbf156b9a7f50af3309057fc197f8d21e8)** – Migrate object detection to MobileNet V3 Large

* **Features**:

  * Upgraded the primary detection model to **SSD-MobileNetV3-Large** for improved accuracy and reduced false positives compared to the previous version.
  * Preserved the original MobileNet V2 implementation for legacy compatibility and testing purposes.

**Key Changes**:

* Replaced MobileNet V2 with **SSD-MobileNetV3-Large** in `detect.py`.
* Renamed the previous V2 detection script to `detect_v2.py`.

---

### **[v1.5.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/7344aed9e06dbc418f4f67e27df90a4a3be01dc1)** – Added AI object detection

* **Features**:

  * Integrated **MobileNet-SSD version 2** to verify **humans and animals** before starting the broadcast, reducing false detections from environmental motion.

**Key Changes**:

* Added `is_target_present` check to filter motion events before initiating streaming.

---

### **[v1.4.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/5bf5c6efccb731db457f1b98d0373f675d730154)** – Integrate YouTube broadcast with camera stream and automate playlist management

* **Features**:

  * Integrated camera stream with **YouTube live broadcasting**.
  * After starting the stream, the system automatically creates a YouTube broadcast, transitions it to live status, and adds the stream to a specified playlist.

**Key Changes**:

* Added logic to create a scheduled YouTube broadcast for the camera stream.
* Implemented automatic transition of the broadcast to live status once the stream starts.
* Added ability to add the live stream to a specified playlist.
* Streamlined the process for starting a YouTube live broadcast directly from the camera stream.

---

### **[v1.3.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/75f996df9958ca5851b45ce35d0b8ae7d46020af)** – Implement automated YouTube live stream creation, scheduling, and playlist integration

* **Features**:

  * Added functionality to automate the creation, scheduling, and management of YouTube live broadcasts.
  * Included a feature to automatically add live broadcasts to a specified playlist after they go live.

**Key Changes**:

* Added `create_stream.py` to handle the creation of live broadcasts on YouTube via the Google API.
* Integrated stream scheduling functionality, allowing broadcasts to be scheduled in advance with specific stream keys.
* Implemented automated transition to live status for broadcasts when the stream is active.
* Added logic to add live broadcasts to playlists upon going live.

---

### **[v1.2.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/77a5239e9b30eb6ba872b2c05875487f24e4f934)** – Major refactor of event triggering logic for scalability

* **Features**:

  * Migrated core logic (FFmpeg process management, stream start/stop, Discord notification) from fragmented Bash scripts to a modular Python system (`start_stream.py`, `stop_stream.py`, `send_webhook.py`).
  * Introduced `config.py` to centralize all camera settings (RTSP URLs, YouTube keys, Discord webhooks).

**Key Changes**:

* Simplified the process for handling multiple cameras by centralizing configurations in a single file.
* Improved maintainability and debugging by using Python scripts instead of Bash.
* Updated the README to document the new Python method alongside legacy Bash implementation.

**Impact**:

* Reduces configuration duplication and simplifies debugging.
* Enables easier scaling and better management of camera streams.

---

### **[v1.1.0](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/tree/71e532ef273aac2603cb364e972c57bea18a61f7)** – Added basic motion detection and alerting

* **Features**:

  * Basic motion detection using `Motion` daemon and IP cameras.
  * No AI filtering or object detection.
  * Sends basic alerts to Discord when motion is detected.
  * One camera stream per one YouTube account.
  * Full Bash scripting for configuration.

---
