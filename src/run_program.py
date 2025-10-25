from src.Gestures.gesture_detector import GestureDetector
from src.Desktop.load_keystroke_mappings import load_keystrokes

default_map = load_keystrokes()
classifier = GestureDetector(default_map)
classifier.run_backend_mainloop()
