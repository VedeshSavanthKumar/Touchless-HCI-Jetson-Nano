import cv2
import mediapipe as mp
import pandas as pd
import os

# CONFIGURATION
FILE_NAME = "gesture_data.csv"
# Lower confidence slightly to detect hands at 50cm distance better
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, 
    min_detection_confidence=0.4, # Helps with distance
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Initialize CSV
if not os.path.exists(FILE_NAME):
    landmarks = []
    for i in range(21):
        landmarks.extend([f'x{i}', f'y{i}'])
    landmarks.append('Label')
    df = pd.DataFrame(columns=landmarks)
    df.to_csv(FILE_NAME, index=False)
    print(f"Created {FILE_NAME}")

# CAMERA SETUP (640x480 for Speed)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

counts = {k: 0 for k in ['0','1','2','3','4','6','5']}
print("--- RECORDER READY ---")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)
    
    status_text = "No Hand Detected"
    color = (0, 0, 255) # Red

    if res.multi_hand_landmarks:
        for lh in res.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, lh, mp_hands.HAND_CONNECTIONS)
            status_text = "Hand Detected (Ready)"
            color = (0, 255, 0) # Green
            
            # Record Data
            key = cv2.waitKey(1) & 0xFF
            if key != 255:
                char = chr(key)
                if char in counts:
                    row = []
                    for lm in lh.landmark:
                        row.extend([lm.x, lm.y])
                    row.append(char)
                    pd.DataFrame([row]).to_csv(FILE_NAME, mode='a', header=False, index=False)
                    counts[char] += 1
                    status_text = f"Recording: {char}"
                    color = (0, 255, 255) # Yellow

    # Record 'No Hand' (5)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('5'):
        row = [0]*42 + ['5']
        pd.DataFrame([row]).to_csv(FILE_NAME, mode='a', header=False, index=False)
        counts['5'] += 1
        status_text = "Recording: No Hand"

    # ON-SCREEN UI (Stats)
    cv2.rectangle(frame, (0,0), (640, 40), (0,0,0), -1) # Top Bar
    cv2.putText(frame, f"Status: {status_text}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    # Show Frame Counts (Bottom Left)
    y_pos = 100
    for k, v in counts.items():
        label = k
        if k=='4': label='4(Rew)'
        if k=='6': label='6(Fwd)'
        cv2.putText(frame, f"Key {label}: {v} frames", (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
        y_pos += 25

    cv2.imshow("Data Recorder (Press 0,1,2,3,4,6,5)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()