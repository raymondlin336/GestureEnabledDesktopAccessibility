from src.gestures.gesture_detector import GestureDetector
from src.desktop.load_keystroke_mappings import load_keystrokes

def run_gesture_program():
    default_map = load_keystrokes()
    classifier = GestureDetector(default_map)
    classifier.run_backend_mainloop()

if __name__ == "__main__":
    run_gesture_program()