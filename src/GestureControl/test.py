import ctypes
import time
from collections import deque
import cv2
import numpy as np
from keystrokes import PressKeys
import mediapipe as mp

# -----------------------------
# Gesture logic
# -----------------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Simple low-pass filter for landmark smoothing
class OneEuro:
    def __init__(self, beta=0.04):
        self.beta = beta
        self.prev = None
    def __call__(self, x):
        if self.prev is None:
            self.prev = x
            return x
        y = self.prev + self.beta * (x - self.prev)
        self.prev = y
        return y


def finger_states(hand_landmarks, handedness_label, img_h, img_w):
    """
    Returns:
      fingers: dict like {'thumb': bool, 'index': bool, ...} for EXTENSION
      meta: dict with extra geometry
    """
    lm = hand_landmarks.landmark
    pts = np.array([[lm[i].x * img_w, lm[i].y * img_h] for i in range(21)], dtype=np.float32)

    # Landmark indices
    TIP = [4, 8, 12, 16, 20]
    PIP = [3, 6, 10, 14, 18]

    fingers = {}

    # --- Non-thumb fingers: "up" if fingertip is above its PIP joint (tip y significantly less than pip y)
    for name, tip_i, pip_i in zip(["index","middle","ring","pinky"], TIP[1:], PIP[1:]):
        tip_y = pts[tip_i, 1]
        pip_y = pts[pip_i, 1]
        fingers[name] = (tip_y < pip_y - 5)  # y grows downward, so "smaller y" = higher / more extended

    # --- Thumb detection (distance from palm, normalized)
    palm_indices = [0, 5, 9, 13, 17]  # wrist + MCPs
    palm_center = pts[palm_indices].mean(axis=0)

    thumb_tip = pts[4]
    index_tip = pts[8]

    # Distances (euclidean)
    thumb_dist = np.linalg.norm(thumb_tip - palm_center)
    index_dist = np.linalg.norm(index_tip - palm_center) + 1e-6  # avoid div by 0

    thumb_extended = (thumb_dist / index_dist) > 1.2  # tuneable threshold

    fingers['thumb'] = bool(thumb_extended)

    # geometry for thumbs_up/thumbs_down classification
    wrist_y = pts[0,1]
    thumb_tip_y = pts[4,1]

    meta = {
        "wrist_y": wrist_y,
        "thumb_tip_y": thumb_tip_y,
        "thumb_extended": thumb_extended,
        "palm_y": palm_center
    }

    return fingers, meta

def classify_pose(fingers_up, meta):
    """
    Decide which *named* gesture we're doing.
    Returns one of:
      'open_palm', 'fist',
      'thumbs_up', 'thumbs_down',
      None
    """

    # Count how many fingers are extended
    count = sum(fingers_up.values())
    print(count)

    # Basic poses
    if count == 5:
        return 'open_palm'

    if count == 0:
        # all curled -> fist
        return 'fist'

    # Thumb logic
    thumb_only = (
        fingers_up.get('thumb', False)
        and not any([fingers_up[k] for k in ['index','middle','ring','pinky']])
    )

    if thumb_only and meta["thumb_extended"]:
        # Compare thumb tip vs wrist vertically
        thumb_tip_y = meta["thumb_tip_y"]
        wrist_y = meta["wrist_y"]
        palm_y = meta["palm_y"]

        # margin so tiny jitters don't flip it
        margin = 50

        print(thumb_tip_y, wrist_y, palm_y)

        if thumb_tip_y < wrist_y - margin:
            return 'thumbs_up'

        if thumb_tip_y > wrist_y + margin:
            return 'thumbs_down'

    # Nothing we care about
    return None


class GestureController:
    def __init__(self):
        self.hand = mp_hands.Hands(static_image_mode=False,
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

    def can_fire(self, key):
        now = time.time()
        ok = (now - self.last_trigger.get(key, 0)) > self.cooldowns.get(key, 0.5)
        if ok:
            self.last_trigger[key] = now
        return ok

    def action(self, gesture):
        if gesture == 'thumbs_up':
            print("Volume up detected")
            PressKeys.volume_up()
        elif gesture == 'thumbs_down':
            print("Volume down detected")
            PressKeys.volume_down()

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
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # finger states
            fingers_up, meta = finger_states(hand_landmarks, handedness or 'Right', h, w)
            gesture_to_fire = classify_pose(fingers_up, meta)

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


def main():
    update_delay = 0.1
    cap = cv2.VideoCapture(1)
    if cap.isOpened():
        cap = cv2.VideoCapture(1)
    else:
        raise SystemExit("Cannot find webcam 1 (external)")

    gc = GestureController()
    print("Running… Press 'q' in the preview window to quit.")

    while True:
        time.sleep(update_delay)
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)  # mirror for more natural control
        frame = gc.process(frame)
        cv2.imshow('Gesture Control', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
