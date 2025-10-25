import math
import numpy as np

class GestureClassifier:
    @staticmethod
    def get_fingers_info(hand_landmarks, img_h, img_w):
        lm = hand_landmarks.landmark
        pts = np.array([[lm[i].x * img_w, lm[i].y * img_h] for i in range(21)], dtype=np.float32)

        # indices for finger tips
        finger_tips_idx = [4, 8, 12, 16, 20]

        fingers = {}

        # --- Thumb detection (distance from palm, normalized)
        palm_indices = [0, 5, 9, 13, 17]  # wrist + MCPs
        palm_center = pts[palm_indices].mean(axis=0)
        palm_y = palm_center[1]
        palm_x = palm_center[0]

        thumb_extended = None
        thumb_up = None

        # Loops through all 5 fingers and collects information.
        # Finger extention calculated by sqrt x and y distance between fingertips and palm.
        for name, tip_i in zip(["thumb", "index", "middle", "ring", "pinky"], finger_tips_idx):
            tip_y = pts[tip_i, 1]
            tip_x = pts[tip_i, 0]
            palm_tip_distance = math.sqrt(((abs(tip_y - palm_y))**2 + (abs(tip_x - palm_x))**2))
            print(name, palm_tip_distance)
            finger_extended = palm_tip_distance > 85
            fingers[name] = finger_extended
            if name == "thumb":
                thumb_extended = finger_extended
                thumb_up = tip_y < palm_y
                print(thumb_up)

        if thumb_up is None or thumb_extended is None:
            print("Thumb not detected correctly.")

        finger_summary_info = {
            "num_extended": sum(fingers.values()),
            "thumb_extended": thumb_extended,
            "thumb_up": thumb_up
        }

        return finger_summary_info

    @staticmethod
    def classify_gesture(summary):

        count = summary["num_extended"]
        print(count)

        if count == 0:
            return 'fist'
        elif count == 1 and summary["thumb_extended"]:
            if summary["thumb_up"]:
                return 'thumbs_up'
            else:
                return 'thumbs_down'
        else:
            return None
