# Motion Detection System with Discord Notifications and YouTube Streaming

This project allows you to set up a **motion detection system** on Unix/Linux servers using [Motion](https://motion-project.github.io/) with **IP cameras**. When motion is detected:

1. A **Discord webhook** notification is sent.
2. A **YouTube live stream** of the camera feed starts.
3. The stream stops automatically when the motion event ends.

No videos or snapshots are saved on the server; all motion detection happens in real-time.

---

## Features

- Real-time motion detection from multiple IP cameras.
- Discord notifications for each motion event.
- Automatic YouTube live streaming while motion is detected.
- Automatic stopping of streams when motion ends.
- Minimal server storage usage, since no files are stored locally.
- Configurable for any number of cameras.

---


---

## Installation Guide

### 1. Install Dependencies

```bash
sudo apt update
sudo apt install motion ffmpeg curl -y
````

### 2. Configure Motion

1. Copy the main configuration to [/etc/motion/motion.conf](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/blob/main/motion.conf).
2. Set daemon mode, disable local storage, and enable emulated motion:

### 3. Camera-Specific Configs

#### Kitchen Camera [/etc/motion/ipcamera-kitchen.conf](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/blob/main/ipcamera-kitchen.conf)

---

## Bash Scripts

All scripts should be **executable**:

```bash
chmod +x PATH TO SCRIPTS/*.sh
```

### 1. Discord Webhook [Script](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/blob/main/webhook-ipcamera-kitchen.sh)

### 2. Start YouTube Stream [Script](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/blob/main/start-ip-camera-kitchen.sh)

### 3. Stop YouTube Stream [Script](https://github.com/ceo-py/Motion-IP-Camera-To-Youtube-Stream/blob/main/stop-ip-camera-kitchen.sh)

---

## Running the System

1. Start Motion as a service:

```bash
sudo systemctl enable motion
sudo systemctl start motion
sudo systemctl status motion
```

2. Verify cameras and logs:

```bash
sudo tail -f /var/log/motion/motion.log
```

* Motion will trigger the Discord webhook and start/stop YouTube streams automatically.

---

## Notes

* Make sure RTSP URLs and YouTube stream keys are correct.
* Logs are stored in `PATH YOU GIVE INSIDE THE STAR CAMERA SCRIPT`.
* Adjust `threshold` and `minimum_motion_frames` per camera for sensitivity.
* Motion handles multiple cameras; each camera has its own `.conf` and scripts.
* Scripts prevent multiple instances of FFmpeg from running simultaneously.
* Use emulate_motion on for testing automation and to verify triggers without physical motion.

