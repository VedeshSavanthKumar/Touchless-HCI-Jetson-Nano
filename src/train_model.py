import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle
import os

DATA_FILE = "gesture_data.csv"
MODEL_FILE = "gesture_model.pkl"

print("--- TRAINING SVM BRAIN (WITH POSITION FIX) ---")

if not os.path.exists(DATA_FILE):
    print("❌ Error: Data file not found.")
    exit()

# 1. Load Data
print("1. Loading Data...")
df = pd.read_csv(DATA_FILE, dtype={'Label': str})
y = df['Label']

print(f"   -> Samples: {len(df)}")
print("2. Normalizing Coordinates (Fixing the Position Trap)...")

# --- THE FIX: RELATIVE COORDINATE NORMALIZATION ---
# This mathematically anchors the wrist (x0, y0) to 0,0
# so the AI only learns the hand shape, not the screen position!
X = pd.DataFrame()
for i in range(21):
    X[f'x{i}'] = df[f'x{i}'] - df['x0']
    X[f'y{i}'] = df[f'y{i}'] - df['y0']

# 3. Split (Stratify for balance)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Train
print("3. Training Model...")
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# 5. Validate
print("4. Validating...")
acc = accuracy_score(y_test, model.predict(X_test))
print(f"   -> EXAM ACCURACY: {acc*100:.2f}%")

# 6. Save
with open(MODEL_FILE, 'wb') as f:
    pickle.dump(model, f)
print("✅ DONE. AI is now Position-Independent!")