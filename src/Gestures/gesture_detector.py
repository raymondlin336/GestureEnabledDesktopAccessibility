import time
import cv2
from src.Desktop.keystrokes import PressKeys
from src.Gestures.gesture_classifier import GestureClassifier
import mediapipe as mp

class Gesture:
    def __init__(self, gesture, function, hexkey):
        self.gesture = gesture
        self.function = function
        self.hexkey = int(hexkey, 16)

    def execute(self):
        PressKeys.press_key(self.hexkey)
        print(self.hexkey)

class GestureDetector:
    def __init__(self, gestures_list):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hand = self.mp_hands.Hands(static_image_mode=False,
                                   max_num_hands=1,
                                   min_detection_confidence=0.6,
                                   min_tracking_confidence=0.6)
        self.last_trigger = {}
        self.cooldowns = {
            'open_palm': 1,
            'fist': 1,
            'thumbs_up': 1,
            'thumbs_down': 1,
        }
        self.gestures_map = {}
        for g in gestures_list:
            gesture, function, hexkey = g["gesture"], g["function"], g["hexkey"]
            self.gestures_map[gesture] = Gesture(gesture, function, hexkey)

    def can_fire(self, key):
        now = time.time()
        ok = (now - self.last_trigger.get(key, 0)) > self.cooldowns.get(key, 0.5)
        if ok:
            self.last_trigger[key] = now
        return ok

    def action(self, gesture):
        self.gestures_map[gesture].execute()

    def process(self, frame, enabled_hud=True, enable_actions=True):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.hand.process(img)
        h, w = frame.shape[:2]
        gesture_to_fire = None
        handedness = None

        if res.multi_hand_landmarks:
            hand_landmarks = res.multi_hand_landmarks[0]
            if res.multi_handedness:
                handedness = res.multi_handedness[0].classification[0].label
            # draw
            self.mp_drawing.draw_landmarks(
                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            # finger states
            summary = GestureClassifier.get_fingers_info(hand_landmarks, h, w)
            gesture_to_fire = GestureClassifier.classify_gesture(summary)

        if enabled_hud:
            cv2.rectangle(frame, (0,0), (350,120), (0,0,0), -1)
            cv2.putText(frame, f"Pose: {gesture_to_fire or '—'}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
            if handedness:
                cv2.putText(frame, f"Hand: {handedness}", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            cv2.putText(frame, "q = quit", (10,95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 1)

        if enable_actions:
            if gesture_to_fire and self.can_fire(gesture_to_fire):
                self.action(gesture_to_fire)

        return frame

    def run_backend_mainloop(self):
        update_delay = 0.1
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap = cv2.VideoCapture(0)
        else:
            raise SystemExit("Cannot find webcam 1 (external)")
        while True:
            time.sleep(update_delay)
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)  # mirror for more natural control
            frame = self.process(frame)
            cv2.imshow('Gesture Control', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
