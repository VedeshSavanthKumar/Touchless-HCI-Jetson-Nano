import sys
import subprocess

def check_package(name, import_name=None):
    """Checks if a Python library is installed and prints its version."""
    if import_name is None:
        import_name = name
    
    try:
        module = __import__(import_name)
        # Try different ways to get the version string
        if hasattr(module, '__version__'):
            version = module.__version__
        elif hasattr(module, 'version'):
            version = module.version
        else:
            version = "Installed (Version unknown)"
        print(f"✅ {name.ljust(15)} : FOUND (v{version})")
        return True
    except ImportError:
        print(f"❌ {name.ljust(15)} : MISSING")
        return False

def check_apt(name):
    """Checks if a Linux system tool (like VLC) is installed via apt."""
    try:
        res = subprocess.run(["dpkg", "-s", name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0:
            print(f"✅ {name.ljust(15)} : INSTALLED")
            return True
        else:
            print(f"❌ {name.ljust(15)} : NOT INSTALLED")
            return False
    except:
        print(f"❌ {name.ljust(15)} : ERROR CHECKING")
        return False

# --- MAIN SCRIPT ---
print("="*40)
print("   JETSON NANO PROJECT ENVIRONMENT CHECK")
print("="*40)

# 1. Check Python Version
print(f"ℹ️  Python System   : {sys.version.split()[0]}")

# 2. Check Python Libraries
required_libs = [
    ("opencv-python", "cv2"),
    ("mediapipe", "mediapipe"),
    ("numpy", "numpy"),
    ("pandas", "pandas"),
    ("scikit-learn", "sklearn"),
    ("pyautogui", "pyautogui"),
]

print("-" * 40)
print("PYTHON LIBRARIES:")
all_good = True
for pkg_name, import_name in required_libs:
    if not check_package(pkg_name, import_name):
        all_good = False

# 3. Check System Tools (VLC, Scrot)
print("-" * 40)
print("SYSTEM TOOLS (Linux Apt):")

if not check_apt("vlc"): all_good = False
if not check_apt("scrot"): all_good = False  # Critical for PyAutoGUI

print("="*40)
if all_good:
    print("🚀 STATUS: SYSTEM READY. You can run the project.")
else:
    print("⚠️  STATUS: MISSING DEPENDENCIES. Please install the missing red items.")
print("="*40)