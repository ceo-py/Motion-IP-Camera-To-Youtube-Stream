
# Motion Detection System with Discord Notifications and YouTube Streaming

This project provides two distinct methods for setting up a real-time motion detection system using the [Motion](https://motion-project.github.io/) daemon and IP cameras. When motion is detected, the system automatically sends a notification and starts a YouTube live stream, which stops when the motion event concludes.

No videos or snapshots are saved on the server; all processing occurs in real-time.

---

## 🚀 Features

* **Real-time** motion detection from multiple IP cameras.
* **Discord notifications** for each motion event.
* **Automatic YouTube live streaming** while motion is detected.
* Automatic stopping of streams when motion ends.
* Minimal server storage usage.
* Highly configurable for any number of cameras.

---

# Method 1: Python System (Recommended for Scalability) 🐍

This method uses centralized configuration (`config.py`) and modular Python scripts (`start_stream.py`, `send_webhook.py`) for easier maintenance and management of multiple cameras.

## 1. Installation Guide (Python)

### Dependencies

You only need `motion` and `ffmpeg`. The Python scripts use **built-in Python libraries** (`subprocess`, `urllib`, `json`).

```bash
sudo apt update
sudo apt install motion ffmpeg python3 -y
````

### Project File Structure

Place the following Python scripts and configuration file in a dedicated directory (e.g., `/PATH/TO/YOUR/SCRIPTS`):

1.  `config.py` (Central source of truth for all URLs, keys, and webhook addresses)
2.  `start_stream.py` (Starts FFmpeg process, saves PID, and sends a "Stream Live" webhook)
3.  `stop_stream.py` (Reads PID, sends kill signal, and removes PID file)
4.  `send_webhook.py` (Reusable function to send motion-triggered alerts)

### Permissions (MANDATORY)

Since your Motion service is running as the **root** user via `systemd`, you must ensure the following are configured correctly:

| **Target** | **Requirement** | **Command**                                 |
| :--- | :--- |:--------------------------------------------|
| **Scripts** (`*.py`) | **Execute** permission & Shebang line | `chmod +x *.py`                             |
| **Log Directory** | Directory must exist | `sudo mkdir -p /PATH/TO/YOUR/SCRIPTS/logs` |

You must add **`#!/usr/bin/env python3`** as the **very first line** of `start_stream.py`, `stop_stream.py`, and `send_webhook.py`.

## 2\. Configuration (`config.py`)

This file contains all camera-specific settings. The Python scripts dynamically load settings based on the camera name passed by Motion.

```python
# config.py (snippet)

LOG_DIR = "/PATH/TO/YOUR/SCRIPTS/logs"
FFMPEG_BIN = "/usr/bin/ffmpeg"

CAMERA_CONFIG = {
    "Kitchen": {
        "STREAM_URL": "rtsp://...",
        "YOUTUBE_KEY": "1234-1234-1234-1234-1234",
        "CHAT_INFO": "Kitchen Live Stream",
        "WEBHOOK_URL": "[https://discord.com/api/webhooks/xxxx",
        "MESSAGE": "🚨 Motion Alert: Kitchen Camera at"
    },
    # Add other cameras here...
}
```

## 3\. Motion Configuration Integration (Python)

In your camera-specific configuration file (e.g., `/etc/motion/ipcamera-kitchen.conf`).
```conf
############################################################
# Event Handling - Python Scripts
############################################################

# Start the stream when motion starts (calls start_stream.py and sends "LIVE" webhook)
on_event_start /usr/bin/python3 /path/to/your/scripts/start_stream.py Kitchen

# Stop the stream when motion ends
on_event_end /usr/bin/python3 /path/to/your/scripts/stop_stream.py Kitchen
```

-----

# Method 2: Legacy Bash System (Individual Scripts) 🐚

This method uses simple, self-contained Bash scripts for each camera. This is less scalable as configuration must be duplicated across multiple files.

## 1\. Installation Guide (Bash)

### Dependencies

This method requires `curl` for webhooks, plus `motion` and `ffmpeg`.

```bash
sudo apt update
sudo apt install motion ffmpeg curl -y
```

### Project File Structure

Place your individual shell scripts (e.g., `webhook-kitchen.sh`, `start-kitchen.sh`, `stop-kitchen.sh`) in your preferred scripts directory.

### Bash Scripts

All scripts should be **executable**:

```bash
chmod +x /path/to/your/scripts/*.sh
```

**CRITICAL:** You must manually update the **Discord Webhook URL**, **RTSP camera URL**, and **YouTube Stream Key** inside **every** individual Bash script file.

## 2\. Motion Configuration Integration (Bash)

In your camera-specific configuration file (e.g., `/etc/motion/ipcamera-kitchen.conf`), use the full path to your Bash scripts.

```conf
############################################################
# Event Handling - Bash Scripts
############################################################

# Start the stream and send a notification
on_event_start /path/to/your/scripts/start-ip-camera-kitchen.sh

# Stop the stream
on_event_end /path/to/your/scripts/stop-ip-camera-kitchen.sh
```

-----

## ⚙️ Running the System (Both Methods)

1.  **Start or restart Motion** to load the new configuration:

    ```bash
    sudo systemctl enable motion
    sudo systemctl restart motion
    sudo systemctl status motion
    ```

2.  **Verify camera logs** for execution success:

    ```bash
    sudo tail -f /var/log/motion/motion.log
    # Check the Python logs for PID files and timestamps (Python Method Only):
    sudo tail -f /PATH/TO/YOUR/SCRIPTS/logs/ffmpeg-Kitchen.log 
    ```

## 📝 Notes

  * **Tuning:** Adjust `threshold` and `minimum_motion_frames` per camera in your Motion config files for correct motion sensitivity.
  * **Testing:** Use `emulate_motion on` in your camera config for testing automation and verifying that triggers are firing without physical motion.



