To get the links to work exactly like that GitHub example, the **anchor link** (the part after the `#`) must match the heading text exactly: lowercase, with hyphens replacing spaces, and **all special characters (like emojis) removed**.

Here is the updated code. I have removed the emojis from the main headings to ensure 100% compatibility with GitHub's `readme-ov-file` redirection logic.

---

```markdown
# 🖐️ Touchless HCI for Media Control on NVIDIA Jetson Nano

An optimized, real-time Human-Computer Interaction (HCI) system built specifically for the **NVIDIA Jetson Nano Developer Kit**. This project translates real-time hand gestures into system-level media control commands for VLC Media Player.

---

## Table of Contents
1. [About The Project](#about-the-project)
2. [Key Performance Metrics](#key-performance-metrics)
3. [Gesture Command Map](#gesture-command-map)
4. [Hardware and Software Requirements](#hardware-and-software-requirements)
5. [Installation and Setup](#installation-and-setup)
6. [Hardware Optimization](#hardware-optimization)
7. [Workflow Data to Inference](#workflow-data-to-inference)
8. [Edge Computing Optimizations](#edge-computing-optimizations)
9. [Project Demo Video](#project-demo-video)

---

## About The Project
This system leverages **MediaPipe Hands** for lightweight 3D landmark extraction and a **Support Vector Machine (SVM)** classifier for robust gesture recognition. It bypasses common edge-computing bottlenecks—such as Out-of-Memory (OOM) crashes and CPU throttling—through strict pipeline optimizations, ensuring high stability for local media control.

### Key Performance Metrics
* **Accuracy:** 95.45% (Achieved via relative coordinate normalization).
* **Latency:** <100ms end-to-end (Achieved via frame skipping).
* **Throughput:** Stable at 15-30 FPS on Jetson Nano hardware.

---

## Gesture Command Map

| Key | Gesture Name | Mapped Action (VLC) | System Execution |
| :--- | :--- | :--- | :--- |
| `1` | **PALM** | UNLOCK / PLAY / PAUSE | `press('space')` |
| `0` | **FIST** | HARD STOP | `press('s')` |
| `2` | **PINCH** | VOLUME UP (+) | `press('volumeup')` |
| `3` | **POINT** | VOLUME DOWN (-) | `press('volumedown')` |
| `4` | **THUMB LEFT** | REWIND (<<) | `press('left')` |
| `6` | **THUMB RIGHT** | FORWARD (>>) | `press('right')` |
| `5` | **NO HAND** | AUTO-LOCK / STANDBY | *System Wait* |

---

## Hardware and Software Requirements
* **Hardware:** NVIDIA Jetson Nano Developer Kit (2GB/4GB), USB Webcam
* **OS:** JetPack OS with CUDA support (Ubuntu 18.04)
* **Software:** Python 3.6, OpenCV, MediaPipe, Scikit-Learn, PyAutoGUI, NumPy
* **Media Player:** VLC Media Player (Optimized for H.264 `.mp4` at 480p/720p)

---

## Installation and Setup

### 1. Install Dependencies
```bash
pip3 install opencv-python mediapipe pandas scikit-learn pyautogui numpy

```

### 2. Install VLC Media Player

```bash
sudo apt-get update && sudo apt-get install vlc -y

```

---

## Hardware Optimization

To ensure maximum performance and avoid OOM (Out-of-Memory) terminations, set the Jetson to MAX power mode:

```bash
sudo nvpmodel -m 0
sudo jetson_clocks

```

---

## Workflow Data to Inference

### Phase 1: Data Collection

Collect custom hand landmarks to build your training dataset.

```bash
python3 record_data.py

```

### Phase 2: Model Training

Train the Scikit-Learn SVM classifier. Coordinates are mathematically normalized relative to the wrist to ensure the model learns the shape of the gesture.

```bash
python3 train_model.py

```

### Phase 3: Live Edge Inference

Run the live controller alongside VLC Media Player.

```bash
python3 vlc_control.py

```

---

## Edge Computing Optimizations

* **Edge Frame Skipping:** The inference loop processes every 2nd frame, preventing the MediaPipe pipeline from bottlenecking the Jetson's CPU.
* **Buffer Bloat Eradication:** `cv2.CAP_PROP_BUFFERSIZE` is hardcoded to 1, preventing OpenCV from queuing old frames.
* **Memory Management:** A 4GB Swapfile was provisioned on the SD card to prevent Linux OOM (Out-of-Memory) crashes.

---

## Project Demo Video

Watch the system in action on YouTube:

> **Note:** Replace `YOUR_VIDEO_ID` with your actual YouTube ID (e.g., `dQw4w9WgXcQ`).

```


Would you like me to help you generate the **`record_data.py`** script so you can start capturing your hand gestures?

```
