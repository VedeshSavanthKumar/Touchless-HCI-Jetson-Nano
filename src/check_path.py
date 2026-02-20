import mediapipe
import os

print(f"1. MediaPipe is loaded from: {mediapipe.__file__}")

try:
    print(f"2. Available attributes: {dir(mediapipe)}")
    print(f"3. Testing Solutions: {mediapipe.solutions}")
    print("SUCCESS: MediaPipe is working.")
except AttributeError as e:
    print(f"FAILURE: {e}")
    print("-> If the path in Step 1 is 'A:\\JETSON PROJECT\\mediapipe.py', RENAME YOUR FILE.")