import math
import numpy as np


class GestureClassifier:
    @staticmethod
    def get_fingers_info(hand_landmarks, img_h, img_w):
        lm = hand_landmarks.landmark
        pts = np.array([[lm[i].x * img_w, lm[i].y * img_h] for i in range(21)], dtype=np.float32)

        # indices for finger tips
        finger_tips_idx = [4, 8, 12, 16, 20]

        fingers_extended = {}
        fingers_closed = {}

        palm_indices = [0, 5, 9, 13, 17]  # wrist + MCPs
        palm_center = pts[palm_indices].mean(axis=0)
        palm_y = palm_center[1]
        palm_x = palm_center[0]
        palm_size = math.sqrt((abs(pts[0, 1] - pts[5, 1]))**2 + (abs(pts[0, 0] - pts[5, 0]))**2)

        thumb_extended = None
        thumb_up = None
        okay_symbol = None

        # Loops through all 5 fingers and collects information.
        # Finger extention calculated by sqrt x and y distance between fingertips and palm.
        for name, tip_i in zip(["thumb", "index", "middle", "ring", "pinky"], finger_tips_idx):
            tip_y = pts[tip_i, 1]
            tip_x = pts[tip_i, 0]
            palm_tip_distance = math.sqrt(((abs(tip_y - palm_y))**2 + (abs(tip_x - palm_x))**2))
            #print(name, palm_tip_distance)
            finger_extended = palm_tip_distance > palm_size * 0.8
            finger_closed = palm_tip_distance < palm_size * 0.6
            fingers_extended[name] = finger_extended
            fingers_closed[name] = finger_closed
            if name == "thumb":
                thumb_extended = finger_extended
                thumb_up = tip_y < palm_y
                #print(thumb_up)
            if name == "index":
                thumb_index_distance = math.sqrt(((abs(pts[4, 0] - tip_x))**2 + (abs(pts[4, 1] - tip_y))**2))
                #print(thumb_index_distance)
                okay_symbol = thumb_index_distance < palm_size * 0.1

        # if thumb_up is None or thumb_extended is None:
        #     print("Thumb not detected correctly.")

        finger_summary_info = {
            "num_extended": sum(fingers_extended.values()),
            "num_closed": sum(fingers_closed.values()),
            "thumb_extended": thumb_extended,
            "thumb_up": thumb_up,
            "okay_symbol": okay_symbol
        }

        return finger_summary_info, palm_size

    @staticmethod
    def classify_gesture(summary):

        print(summary["num_extended"], summary["num_closed"])

        if summary["okay_symbol"] == True and summary["num_extended"] == 5:
            return "end_loop"
        elif summary["num_closed"] == 5:
            return 'fist'
        elif summary["num_extended"] == 1 and summary["thumb_extended"]:
            if summary["thumb_up"]:
                return 'thumbs_up'
            else:
                return 'thumbs_down'
        else:
            return None
