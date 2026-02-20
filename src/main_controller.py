import cv2
import mediapipe as mp
import pickle
import numpy as np
import pyautogui
import time
import warnings

# --- CONFIGURATION ---
MODEL_FILE = "gesture_model.pkl"
CONFIDENCE_THRESHOLD = 0.5   # 50% Confidence required
LOCK_TIMEOUT = 10.0          # Auto-lock after 10s of no hand
# ---------------------

# 1. SILENCE WARNINGS (Fixes the red text spam)
warnings.filterwarnings("ignore")

print("1. Loading AI Brain...")
try:
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
    print("   -> Model Loaded Successfully!")
except Exception as e:
    print(f"ERROR: Could not load model. {e}")
    exit()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# State Variables
is_locked = False
last_hand_time = time.time()
prev_y = 0
prev_action_time = 0

# Labels must match your training data
LABELS = {
    '0': 'FIST', 
    '1': 'PALM', 
    '2': 'PINCH', 
    '3': 'POINT', 
    '5': 'NO_HAND'
}

cap = cv2.VideoCapture(0)

print("--- SYSTEM READY ---")
print("1. Focus your VLC window.")
print("2. Show PALM to start.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process Hand
    results = hands.process(rgb_frame)
    
    current_gesture = "NO_HAND"
    confidence_text = "0%"
    
    if results.multi_hand_landmarks:
        last_hand_time = time.time()
        
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract Coordinates
            row = []
            for lm in hand_landmarks.landmark:
                row.extend([lm.x, lm.y])
            
            # Predict
            prediction = model.predict([row])[0]
            probability = np.max(model.predict_proba([row]))
            
            # Format output
            gesture_name = LABELS.get(prediction, "UNKNOWN")
            confidence_text = f"{int(probability * 100)}%"
            
            if probability > CONFIDENCE_THRESHOLD:
                current_gesture = gesture_name
                current_y = hand_landmarks.landmark[8].y  # Index finger tip

    # --- LOGIC ENGINE ---
    
    # 1. Auto-Lock Logic
    if time.time() - last_hand_time > LOCK_TIMEOUT:
        is_locked = True
    
    if is_locked:
        # RED BORDER
        cv2.rectangle(frame, (0,0), (width, height), (0, 0, 255), 10)
        cv2.putText(frame, "LOCKED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        if current_gesture == 'PALM':
            is_locked = False
            print("Action: SYSTEM UNLOCKED")
            
    else:
        # GREEN BORDER
        cv2.rectangle(frame, (0,0), (width, height), (0, 255, 0), 10)
        
        # Display Gesture & Accuracy on Screen
        status_text = f"{current_gesture} ({confidence_text})"
        cv2.putText(frame, status_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 2. Action Logic (Debounced)
        if time.time() - prev_action_time > 0.5:
            
            if current_gesture == 'FIST':
                pyautogui.press('space')
                print(f"Action: PAUSE/PLAY ({confidence_text})")
                prev_action_time = time.time()
                
            elif current_gesture == 'POINT':
                pyautogui.press('right')
                print(f"Action: SEEK ({confidence_text})")
                prev_action_time = time.time() - 0.2
                
            elif current_gesture == 'PINCH':
                if abs(current_y - prev_y) > 0.03:
                    if current_y < prev_y: 
                        pyautogui.hotkey('ctrl', 'up')
                        print("Action: VOL UP")
                    else: 
                        pyautogui.hotkey('ctrl', 'down')
                        print("Action: VOL DOWN")
                prev_action_time = time.time() - 0.1
                prev_y = current_y

    cv2.imshow('Touchless Interface', frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()