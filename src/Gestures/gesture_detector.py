import time
import cv2
from src.Desktop.keystrokes import PressKeys
from src.Gestures.gesture_classifier import GestureClassifier
import mediapipe as mp
from collections import deque

class Gesture:
    def __init__(self, gesture, function, hexkeys):
        self.gesture = gesture
        self.function = function
        self.hexkeys = [int(hk, 16) for hk in hexkeys]

    def execute(self):
        for hk in self.hexkeys:
            PressKeys.press_key(hk)
        for hk in self.hexkeys:
            PressKeys.release_key(hk)

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
            'fist': 1,
            'thumbs_up': 0.4,
            'thumbs_down': 0.4,
        }
        self.gestures_map = {}
        for g in gestures_list:
            gesture, function, hexkey = g["gesture"], g["function"], g["hexkey"]
            self.gestures_map[gesture] = Gesture(gesture, function, hexkey)

        self.motion_history = deque(maxlen=5)

    def can_fire(self, key):
        now = time.time()
        ok = (now - self.last_trigger.get(key, 0)) > self.cooldowns.get(key, 0.5)
        if ok:
            self.last_trigger[key] = now
        return ok

    def action(self, gesture):
        self.gestures_map[gesture].execute()

    def detect_swipe(self, h, w, hand_landmarks, summary):
        """
        Returns 'swipe_left', 'swipe_right', or None
        """

        # get wrist coordinates in pixel space
        lm = hand_landmarks.landmark
        wrist_x = lm[0].x * w
        t_now = time.time()

        # save (time, x)
        self.motion_history.append((t_now, wrist_x))

        # need enough history to compare
        if len(self.motion_history) < 2:
            return None

        # compare oldest vs newest
        t_start, x_start = self.motion_history[0]
        t_end, x_end = self.motion_history[-1]

        dt = t_end - t_start
        dx = x_end - x_start  # +dx == moved right on screen, -dx == left

        # tune these:
        SWIPE_TIME = 0.25      # sec window for a "fast" swipe
        SWIPE_PIXELS = 120.0   # how far (in pixels) counts as a swipe

        # optional guard: require open hand so random movement doesn't trigger
        hand_open_enough = summary["num_extended"] >= 4

        if dt <= SWIPE_TIME and hand_open_enough:
            if dx > SWIPE_PIXELS:
                return "swipe_right"
            elif dx < -SWIPE_PIXELS:
                return "swipe_left"

        return None

    def process(self, frame, enabled_hud=True, enable_actions=True):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.hand.process(img)
        h, w = frame.shape[:2]
        gesture_to_fire = None
        handedness = None

        if res.multi_hand_landmarks:
            print("========================================")
            hand_landmarks = res.multi_hand_landmarks[0]
            if res.multi_handedness:
                handedness = res.multi_handedness[0].classification[0].label

            # draw landmarks
            self.mp_drawing.draw_landmarks(
                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            # static finger-open type gesture
            summary = GestureClassifier.get_fingers_info(hand_landmarks, h, w)
            static_gesture = GestureClassifier.classify_gesture(summary)

            # motion-based gesture (swipe)
            swipe_gesture = self.detect_swipe(h, w, hand_landmarks, summary)

            # priority: swipes override static poses if swipe exists that frame
            gesture_to_fire = swipe_gesture if swipe_gesture else static_gesture

        else:
            # no hand visible -> reset motion history so old motion
            # doesn’t falsely trigger when hand reappears
            self.motion_history.clear()

        # HUD
        if enabled_hud:
            cv2.rectangle(frame, (0, 0), (350, 140), (0, 0, 0), -1)
            cv2.putText(frame, f"Pose: {gesture_to_fire or '—'}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            if handedness:
                cv2.putText(frame, f"Hand: {handedness}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "q = quit", (10, 95),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            cv2.putText(frame, "swipe = desktops", (10, 125),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # actually act
        if enable_actions:
            if gesture_to_fire and self.can_fire(gesture_to_fire):
                self.action(gesture_to_fire)

        return frame

    def run_backend_mainloop(self):
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap = cv2.VideoCapture(0)
        else:
            raise SystemExit("Cannot find webcam 1 (external)")
        while True:
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
