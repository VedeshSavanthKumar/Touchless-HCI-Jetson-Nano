# 🖐️ Touchless HCI for Media Control on NVIDIA Jetson Nano

An optimized, real-time Human-Computer Interaction (HCI) system built specifically for the **NVIDIA Jetson Nano Developer Kit**. This project translates real-time hand gestures into system-level media control commands for VLC Media Player, achieving **>95% accuracy** and **sub-100ms latency** on edge hardware.

---

## 📌 Table of Contents
* [Project Overview](#project-overview)
* [Key Performance Metrics](#performance-metrics)
* [Gesture Command Map](#gesture-map)
* [Requirements and Software](#requirements)
* [Installation and Setup](#installation)
* [Hardware Optimization](#hardware-optimization)
* [Workflow: Data to Inference](#workflow)
* [Edge Computing Optimizations](#edge-optimizations)
* [Project Demo](#demo)

---

<a name="project-overview"></a>
## 📝 Project Overview
This system leverages **MediaPipe Hands** for lightweight 3D landmark extraction and a **Support Vector Machine (SVM)** classifier for robust gesture recognition. It bypasses common edge-computing bottlenecks—such as Out-of-Memory (OOM) crashes and CPU throttling—through strict pipeline optimizations, ensuring high stability for local media control.

---

<a name="performance-metrics"></a>
## 🚀 Key Performance Metrics
* **Accuracy:** 95.45% (Achieved via relative coordinate normalization to eliminate spatial location bias).
* **Latency:** <100ms end-to-end (Achieved via frame skipping and zero-buffer camera configuration).
* **Throughput:** Stable at 15-30 FPS on Jetson Nano hardware.

---

<a name="gesture-map"></a>
## 🎮 Gesture Command Map

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

<a name="requirements"></a>
## 🛠️ Requirements & Software
* **Hardware:** NVIDIA Jetson Nano Developer Kit (2GB/4GB), USB Webcam
* **OS:** JetPack OS with CUDA support (Ubuntu 18.04)
* **Software:** Python 3.6, OpenCV, MediaPipe, Scikit-Learn, PyAutoGUI, NumPy
* **Media Player:** VLC Media Player (Optimized for H.264 `.mp4` at 480p/720p)

---

<a name="installation"></a>
## ⚙️ Installation & Setup

### 1. Install Dependencies
```bash
pip3 install opencv-python mediapipe pandas scikit-learn pyautogui numpy

```

### 2. Configure VLC

```bash
sudo apt-get update
sudo apt-get install vlc

```

---

<a name="hardware-optimization"></a>

## ⚡ Hardware Optimization

To ensure maximum performance and avoid OOM (Out-of-Memory) terminations, set the Jetson to MAX power mode and enable the fan:

```bash
# Set to MAX Power Mode
sudo nvpmodel -m 0

# Enable maximum clock speeds
sudo jetson_clocks

```

---

<a name="workflow"></a>

## 🔄 Workflow: Data to Inference

### Phase 1: Data Collection

Collect custom hand landmarks to build your training dataset.

```bash
python3 record_data.py

```

### Phase 2: Model Training

Train the Scikit-Learn SVM classifier. Coordinates are mathematically normalized relative to the wrist () to ensure the model learns shape rather than position.

```bash
python3 train_model.py

```

### Phase 3: Live Edge Inference

Run the live controller alongside VLC Media Player.

```bash
python3 vlc_control.py

```

---

<a name="edge-optimizations"></a>

## 🛠️ Edge Computing Optimizations

* **Edge Frame Skipping:** The inference loop processes every 2nd frame, preventing CPU bottlenecking.
* **Buffer Bloat Eradication:** `cv2.CAP_PROP_BUFFERSIZE` is hardcoded to 1, preventing OpenCV from queuing old frames.
* **Memory Management:** A 4GB Swapfile was provisioned on the SD card to prevent Linux OOM crashes.

---

<a name="demo"></a>





=========================================================
 🎯 TARGET VS. ACHIEVED: PERFORMANCE METRICS
=========================================================

1. GESTURE ACCURACY (Higher is better)
Required Target : ██████████████████░░  >90.0%
Our Project     : ███████████████████▌   95.4% 🏆

2. SYSTEM LATENCY (Lower is better)
Maximum Allowed : ████████████████████  <200 ms
Our Project     : ████████              ~80 ms 🏆
*(Reduced via Edge Frame Skipping & Zero-Buffer Camera)*

3. PROCESSING SPEED (Higher is better)
Required Target : ███████████████░░░░░  ≥15 FPS
Our Project     : ████████████████████   30 FPS 🏆
*(Stable throughput achieved via Hardware Unthrottling)*

=========================================================
## 📺 Project Demo

Check out the system in action by clicking the preview below:
https://youtu.be/P46tSpa8ddY



---


