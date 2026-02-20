# 🖐️ Touchless HCI for Media Control on NVIDIA Jetson Nano

An optimized, real-time Human-Computer Interaction (HCI) system built specifically for the **NVIDIA Jetson Nano Developer Kit**. This project translates real-time hand gestures into system-level media control commands for VLC Media Player, achieving **>95% accuracy** and **sub-100ms latency** on edge hardware.

---

## 📝 Project Overview
This system leverages **MediaPipe Hands** for lightweight 3D landmark extraction and a **Support Vector Machine (SVM)** classifier for robust gesture recognition. It bypasses common edge-computing bottlenecks—such as Out-of-Memory (OOM) crashes and CPU throttling—through strict pipeline optimizations, ensuring high stability for local media control.

### 🚀 Key Performance Metrics
*   **Accuracy:** 95.45% (Achieved via relative coordinate normalization to eliminate spatial location bias).
*   **Latency:** <100ms end-to-end (Achieved via frame skipping and zero-buffer camera configuration).
*   **Throughput:** Stable at 15-30 FPS on Jetson Nano hardware.

---

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

## 🛠️ Hardware & Software Requirements
*   **Hardware:** NVIDIA Jetson Nano Developer Kit (2GB/4GB), USB Webcam
*   **OS:** JetPack OS with CUDA support (Ubuntu 18.04)
*   **Software:** Python 3.6, OpenCV, MediaPipe, Scikit-Learn, PyAutoGUI, NumPy
*   **Media Player:** VLC Media Player (Optimized for H.264 `.mp4` at 480p/720p)

---

## ⚙️ Installation & Setup

### 1. Install Dependencies
```bash
pip3 install opencv-python mediapipe pandas scikit-learn pyautogui numpy


##2. Optimize Jetson Hardware
To ensure maximum performance and avoid OOM (Out-of-Memory) terminations, set the Jetson to MAX power mode:

sudo nvpmodel -m 0
sudo jetson_clocks


Phase 1: Data Collection
Collect custom hand landmarks to build your training dataset.
python3 record_data.py


Phase 2: Model Training
Train the Scikit-Learn SVM classifier. Coordinates are mathematically normalized relative to the wrist (
) to ensure the model learns the shape of the gesture rather than its position on the screen.
python3 train_model.py

Phase 3: Live Edge Inference
Run the live controller alongside VLC Media Player.
python3 vlc_control.py


Open VLC Player and load an MP4 video.
Click inside the VLC window to make it active.
Show your PALM to unlock the security state and begin controlling the media.
Edge Computing Optimizations
Edge Frame Skipping: The inference loop processes every 2nd frame, preventing the MediaPipe pipeline from bottlenecking the Jetson's CPU.
Buffer Bloat Eradication: cv2.CAP_PROP_BUFFERSIZE is hardcoded to 1, preventing OpenCV from queuing old frames and causing latency buildup.
Memory Management: A 4GB Swapfile was provisioned on the SD card to prevent Linux OOM (Out-of-Memory) crashes during live inference.
