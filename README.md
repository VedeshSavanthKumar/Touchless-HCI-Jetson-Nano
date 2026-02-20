It seems the automatic "slug" generation for the headings might still be clashing with how your specific Markdown viewer handles the links. To fix this permanently, I have implemented **HTML Anchors**.

By placing `<div id="section-name"></div>` tags above each topic, the links will now point to a specific "ID" rather than relying on the heading text. This is the most robust way to ensure redirection works every time.

---

```markdown
# 🖐️ Touchless HCI for Media Control on NVIDIA Jetson Nano

An optimized, real-time Human-Computer Interaction (HCI) system built specifically for the **NVIDIA Jetson Nano Developer Kit**. This project translates real-time hand gestures into system-level media control commands for VLC Media Player.

---

## Table of Contents
* [About The Project](#about)
* [Key Performance Metrics](#metrics)
* [Gesture Command Map](#gestures)
* [Hardware and Software Requirements](#requirements)
* [Installation and Setup](#setup)
* [Hardware Optimization](#optimization)
* [Workflow Data to Inference](#workflow)
* [Edge Computing Optimizations](#edge-optimizations)
* [Project Demo Video](#demo)

---

<div id="about"></div>

## About The Project
This system leverages **MediaPipe Hands** for lightweight 3D landmark extraction and a **Support Vector Machine (SVM)** classifier for robust gesture recognition. It bypasses common edge-computing bottlenecks—such as Out-of-Memory (OOM) crashes and CPU throttling.

---

<div id="metrics"></div>

## Key Performance Metrics
* **Accuracy:** 95.45% (Achieved via relative coordinate normalization).
* **Latency:** <100ms end-to-end (Achieved via frame skipping).
* **Throughput:** Stable at 15-30 FPS on Jetson Nano hardware.

---

<div id="gestures"></div>

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

<div id="requirements"></div>

## Hardware and Software Requirements
* **Hardware:** NVIDIA Jetson Nano Developer Kit (2GB/4GB), USB Webcam
* **OS:** JetPack OS with CUDA support (Ubuntu 18.04)
* **Software:** Python 3.6, OpenCV, MediaPipe, Scikit-Learn, PyAutoGUI, NumPy
* **Media Player:** VLC Media Player

---

<div id="setup"></div>

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

<div id="optimization"></div>

## Hardware Optimization

To ensure maximum performance and avoid OOM (Out-of-Memory) terminations, set the Jetson to MAX power mode:

```bash
sudo nvpmodel -m 0
sudo jetson_clocks

```

---

<div id="workflow"></div>

## Workflow Data to Inference

### Phase 1: Data Collection

```bash
python3 record_data.py

```

### Phase 2: Model Training

Train the Scikit-Learn SVM classifier. Coordinates are mathematically normalized relative to the wrist ().

```bash
python3 train_model.py

```

### Phase 3: Live Edge Inference

```bash
python3 vlc_control.py

```

---

<div id="edge-optimizations"></div>

## Edge Computing Optimizations

* **Frame Skipping:** Processes every 2nd frame to prevent CPU bottlenecking.
* **Buffer Management:** `cv2.CAP_PROP_BUFFERSIZE` set to 1 to eliminate lag.
* **Memory Management:** A 4GB Swapfile is recommended for stability.

---

<div id="demo"></div>

