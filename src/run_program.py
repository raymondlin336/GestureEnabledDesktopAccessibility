from src.gestures.gesture_detector import GestureDetector
from src.desktop.load_keystroke_mappings import load_keystrokes

default_map = load_keystrokes()
classifier = GestureDetector(default_map)
classifier.run_backend_mainloop()
