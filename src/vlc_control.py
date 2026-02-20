import cv2
import mediapipe as mp
import pickle
import numpy as np
import pyautogui
import time
import warnings
from collections import deque

warnings.filterwarnings("ignore")

# 1. LOAD MODEL
try:
    with open("gesture_model.pkl", 'rb') as f:
        model = pickle.load(f)
except:
    print("❌ ERROR: Run train_model.py first!")
    exit()

# 2. SETUP MEDIAPIPE 
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1, 
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# 3. CAMERA (Hardware Optimized)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG')) # Forces fast decoding
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# 4. LOGIC VARS
is_locked = True
last_action = 0
history = deque(maxlen=2) # Instant reactions

COOLDOWNS = {
    '0': 1.5, '1': 1.5, 
    '2': 0.1, '3': 0.1, 
    '4': 0.8, '6': 0.8
}

GESTURE_NAMES = {
    '0': 'STOP (Fist)',
    '1': 'UNLOCK/PLAY (Palm)',
    '2': 'VOL UP (Pinch)',
    '3': 'VOL DOWN (Point)',
    '4': 'REWIND (Thumb L)',
    '6': 'FORWARD (Thumb R)',
    '5': 'NO HAND'
}

print("--- JETSON: EXAM-READY MODE ACTIVE ---")

frame_count = 0
last_gesture = "SEARCHING..."
acc_level = "0%"
prev_frame_time = 0

while cap.isOpened():
    start_time = time.time()
    ret, img = cap.read()
    if not ret: break
    
    frame_count += 1
    img = cv2.flip(img, 1)
    
    # --- LATENCY FIX: EDGE FRAME SKIPPING ---
    if frame_count % 2 == 0: 
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)
        
        if res.multi_hand_landmarks:
            for lh in res.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, lh, mp_hands.HAND_CONNECTIONS)
                
                # --- ACCURACY FIX: NORMALIZED MATH ---
                # Anchor coordinates to the wrist (same as training)
                wrist_x = lh.landmark[0].x
                wrist_y = lh.landmark[0].y
                
                data = []
                for lm in lh.landmark:
                    data.extend([lm.x - wrist_x, lm.y - wrist_y])
                
                try:
                    probs = model.predict_proba([data])[0]
                    idx = np.argmax(probs)
                    raw_pred = str(model.classes_[idx])
                    conf = np.max(probs)
                    
                    acc_level = f"{int(conf*100)}%"
                    
                    if conf > 0.60:
                        history.append(raw_pred)
                    else:
                        history.append("UNCERTAIN")
                    
                    if history.count(history[-1]) == 2 and history[-1] != "UNCERTAIN":
                        stable_pred = history[-1]
                        last_gesture = GESTURE_NAMES.get(stable_pred, "Unknown")
                        
                        if is_locked:
                            if stable_pred == '1': # Unlock on Palm
                                is_locked = False
                                history.clear()
                                print("✅ UNLOCKED")
                        else:
                            now = time.time()
                            if now - last_action > COOLDOWNS.get(stable_pred, 1.0):
                                if stable_pred == '1': pyautogui.press('space')
                                elif stable_pred == '0': pyautogui.press('space')
                                elif stable_pred == '2': pyautogui.press('volumeup')
                                elif stable_pred == '3': pyautogui.press('volumedown')
                                elif stable_pred == '4': pyautogui.press('left')
                                elif stable_pred == '6': pyautogui.press('right')
                                
                                if stable_pred != '5':
                                    last_action = now
                                    print(f"Action: {last_gesture}")
                except: pass
        else:
            last_gesture = "NO HAND"
            acc_level = "0%"

    # --- PERFORMANCE METRICS ---
    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000
    fps = 1 / (end_time - prev_frame_time) if prev_frame_time > 0 else 0
    prev_frame_time = end_time

    # DRAW UI
    cv2.rectangle(img, (0,0), (640, 60), (0,0,0), -1)
    cv2.rectangle(img, (0,60), (640, 90), (30,30,30), -1)
    
    status = "SYSTEM LOCKED (Show Palm)" if is_locked else f"CMD: {last_gesture}"
    color = (0, 0, 255) if is_locked else (0, 255, 0)

    cv2.putText(img, status, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.putText(img, f"Conf: {acc_level}", (480, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    latency_color = (0, 255, 0) if latency_ms < 80 else (0, 0, 255)
    cv2.putText(img, f"FPS: {int(fps)} | Latency: {int(latency_ms)} ms", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, latency_color, 2)

    cv2.imshow("Jetson Controller", img)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()