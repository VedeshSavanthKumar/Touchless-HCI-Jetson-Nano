This is a revamped, professional `README.md` for your project. I’ve restructured it into logical sections, cleaned up the code blocks for easy "one-click" copying, and added the navigation and demo placeholders you requested.

---

# 🖐️ Touchless HCI for Media Control on NVIDIA Jetson Nano

An optimized, real-time Human-Computer Interaction (HCI) system built specifically for the **NVIDIA Jetson Nano**. This project translates hand gestures into system-level media commands for VLC, achieving **>95% accuracy** and **sub-100ms latency** on edge hardware.

---

## 📌 Table of Contents
1. [Project Overview](#project-overview)
2. [Key Performance Metrics](#key-performance-metrics)
3. [Gesture Command Map](#gesture-command-map)
4. [Hardware & Software Requirements](#hardware--software-requirements)
5. [Installation & Setup](#installation--setup)
6. [Hardware Optimization](#hardware-optimization)
7. [Workflow: Data to Inference](#workflow-data-to-inference)
8. [Edge Computing Optimizations](#edge-computing-optimizations)
9. [Project Demo Video](#project-demo-video)
---

## 📝 Project Overview

This system leverages **MediaPipe Hands** for lightweight 3D landmark extraction and a **Support Vector Machine (SVM)** classifier for robust gesture recognition. It bypasses common edge-computing bottlenecks—such as Out-of-Memory (OOM) crashes and CPU throttling—through strict pipeline optimizations.

### 🚀 Key Performance Metrics

* **Accuracy:** 95.45% (Achieved via relative coordinate normalization).
* **Latency:** <100ms end-to-end (Achieved via frame skipping).
* **Throughput:** Stable at 15-30 FPS on Jetson Nano.

---

## 🎮 Gesture Command Map

| Key | Gesture Name | Mapped Action (VLC) | System Execution |
| --- | --- | --- | --- |
| `1` | **PALM** | UNLOCK / PLAY / PAUSE | `press('space')` |
| `0` | **FIST** | HARD STOP | `press('s')` |
| `2` | **PINCH** | VOLUME UP (+) | `press('volumeup')` |
| `3` | **POINT** | VOLUME DOWN (-) | `press('volumedown')` |
| `4` | **THUMB LEFT** | REWIND (<<) | `press('left')` |
| `6` | **THUMB RIGHT** | FORWARD (>>) | `press('right')` |
| `5` | **NO HAND** | AUTO-LOCK / STANDBY | *System Wait* |

---

## 🛠️ Requirements & Software

* **Hardware:** NVIDIA Jetson Nano (2GB/4GB), USB Webcam.
* **OS:** JetPack OS (Ubuntu 18.04).
* **Media Player:** VLC Media Player (Optimized for H.264 `.mp4`).
* **Python Version:** 3.6+

---

## ⚙️ Installation & Setup

### 1. Install Dependencies

Run the following command to install the necessary Python libraries:

```bash
pip3 install opencv-python mediapipe pandas scikit-learn pyautogui numpy

```

### 2. Configure VLC

Ensure VLC is installed and set as your default player:

```bash
sudo apt-get update
sudo apt-get install vlc

```

---

## ⚡ Hardware Optimization

To ensure maximum performance and avoid OOM (Out-of-Memory) terminations, set the Jetson to **MAX power mode** and enable the fan:

```bash
# Set to MAX Power Mode
sudo nvpmodel -m 0

# Enable maximum clock speeds
sudo jetson_clocks

```

---

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

Run the live controller. Ensure VLC is open and the window is active.

```bash
python3 vlc_control.py

```

---

## 🛠️ Edge Computing Optimizations

* **Frame Skipping:** The inference loop processes every 2nd frame, preventing the MediaPipe pipeline from bottlenecking the CPU.
* **Buffer Management:** `cv2.CAP_PROP_BUFFERSIZE` is hardcoded to **1**, preventing the webcam from queuing old frames and causing "laggy" input.
* **Memory Management:** We recommend provisioning a **4GB Swapfile** on the SD card to prevent Linux OOM crashes during long sessions.

---

## 📺 Project Demo

Check out the system in action below:

> **Note:** Click the image above to view the full demonstration of the low-latency gesture control.
