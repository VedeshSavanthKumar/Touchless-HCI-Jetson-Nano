 Touchless HCI for Media Control on NVIDIA Jetson Nano
An optimized, real-time Human-Computer Interaction (HCI) system built specifically for the NVIDIA Jetson Nano Developer Kit. This project translates real-time hand gestures into system-level media control commands for VLC Media Player, achieving >95% accuracy and sub-100ms latency on edge hardware.
📝 Project Overview
This system leverages MediaPipe Hands for lightweight 3D landmark extraction and a Support Vector Machine (SVM) classifier for robust gesture recognition. It bypasses common edge-computing bottlenecks—such as Out-of-Memory (OOM) crashes and CPU throttling—through strict pipeline optimizations, ensuring high stability for local media control.
🚀 Key Performance Metrics
Accuracy: 95.45% (Achieved via relative coordinate normalization to eliminate spatial location bias).
Latency: <100ms end-to-end (Achieved via frame skipping and zero-buffer camera configuration).
Throughput: Stable at 15-30 FPS on Jetson Nano hardware.
🎮 Gesture Command Map
Gesture Name	Mapped Action (VLC)	System Execution (pyautogui)
PALM	UNLOCK / PLAY / PAUSE	press('space')
FIST	HARD STOP	press('s')
PINCH	VOLUME UP (+)	press('volumeup')
POINT	VOLUME DOWN (-)	press('volumedown')
THUMB LEFT	REWIND (<<)	press('left')
THUMB RIGHT	FORWARD (>>)	press('right')
NO HAND	AUTO-LOCK / STANDBY	System Wait
🛠️ Hardware & Software Requirements
Hardware: NVIDIA Jetson Nano Developer Kit (2GB/4GB), USB Webcam.
OS: JetPack OS with CUDA support (Ubuntu 18.04).
Libraries: Python 3.6, OpenCV, MediaPipe, Scikit-Learn, PyAutoGUI, NumPy.
Media Player: VLC Media Player (Optimized for H.264 .mp4 at 480p/720p).
⚙️ Installation & Setup
1. Install Dependencies
bash
pip3 install opencv-python mediapipe pandas scikit-learn pyautogui numpy
Use code with caution.

2. Optimize Jetson Hardware
To ensure maximum performance and avoid OOM (Out-of-Memory) terminations, set the Jetson to MAX power mode:
bash
sudo nvpmodel -m 0
sudo jetson_clocks
Use code with caution.

🔄 The Pipeline: From Data to Control
Phase 1: Data Collection
Collect custom hand landmarks to build your training dataset.
bash
python3 record_data.py
Use code with caution.

Phase 2: Model Training
Train the Scikit-Learn SVM classifier. Coordinates are normalized relative to the wrist 
 for position-independent accuracy.
bash
python3 train_model.py
Use code with caution.

Phase 3: Live Edge Inference
Run the controller alongside VLC. Open VLC, load a video, and ensure the window is active.
bash
python3 vlc_control.py
Use code with caution.

🧠 Edge Computing Optimizations
Frame Skipping: Processes every 2nd frame to prevent CPU bottlenecking.
Buffer Management: cv2.CAP_PROP_BUFFERSIZE is set to 1 to eliminate "buffer bloat" and lag.
Memory Safety: Includes a 4GB Swapfile configuration to prevent Linux OOM crashes during inference.
