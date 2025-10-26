import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = None


def init_hands():
    global hands
    if hands is None:
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )


def process_hand_frame(frame):
    """
    Gets landmarks 0 to 21 of the hand from each frame and returns a tuple for annotated_frame, landmarks_list, and handedness_list
    """
    global hands

    if hands is None:
        init_hands()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    annotated_frame = frame.copy()

    landmarks_list = []
    handedness_list = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(  # landmarks
                annotated_frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            landmarks_list.append(hand_landmarks.landmark)  # stores landmarks

    if results.multi_handedness:  # checks hands
        for handedness in results.multi_handedness:
            handedness_list.append(handedness.classification[0].label)

    return annotated_frame, landmarks_list, handedness_list


def get_hand_position(landmarks, frame_dimensions):
    """
    Uses landmarks to get hand position and returns the (x,y) of the hand's position
    """
    if not landmarks:
        return None, None

    wrist = landmarks[0]
    height, width = frame_dimensions[:2]

    x = int(wrist.x * width)
    y = int(wrist.y * height)

    return x, y


def cleanup_hands():
    global hands
    if hands is not None:
        hands.close()
        hands = None
