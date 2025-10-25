import cv2
import math
import time
import mediapipe as mp
import get_hand
from src.get_hand import hands
from src.get_webcam_open import landmarks

start_time = None

def landmark_distance(landmarkA, landmarkB):
    return math.sqrt((landmarkA.x - landmarkB.x) ** 2 + (landmarkA.y - landmarkB.y) ** 2)

def click(landmarkA_id, landmarkB_id, touching_threshold = 0.05, holding_time=0.5):

    global start_time
    distance = landmark_distance(landmarkA_id, landmarkB_id)

    if distance <= touching_threshold:
        if (start_time is None):
            start_time = time.time()
        elif (time.time() - start_time >= holding_time):
            start_time = None
            print("click")
            return True
    else:
        start_time = None

    return False

def right_click(landmarkA_id, landmarkB_id, touching_threshold = 0.05, holding_time=0.5):

    global start_time
    distance = landmark_distance(landmarkA_id, landmarkB_id)

    if distance <= touching_threshold:
        if (start_time is None):
            start_time = time.time()
        elif (time.time() - start_time >= holding_time):
            start_time = None
            print("right click")
            return True
    else:
        start_time = None

    return False

def left_click(landmarkA_id, landmarkB_id, touching_threshold = 0.05, holding_time=0.5):

    global start_time
    distance = landmark_distance(landmarkA_id, landmarkB_id)

    if distance <= touching_threshold:
        if (start_time is None):
            start_time = time.time()
        elif (time.time() - start_time >= holding_time):
            start_time = None
            print("left click")
            return True
    else:
        start_time = None

    return False

def double_click(landmarkA_id, landmarkB_id, touching_threshold = 0.05, holding_time=0.5):

    global start_time
    distance = landmark_distance(landmarkA_id, landmarkB_id)

    if distance <= touching_threshold:
        if (start_time is None):
            start_time = time.time()
        elif (time.time() - start_time >= holding_time):
            start_time = None
            print("double click")
            return True
    else:
        start_time = None

    return False