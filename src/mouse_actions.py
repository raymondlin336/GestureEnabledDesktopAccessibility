import cv2
import math
import time
import mediapipe as mp
import get_hand
from src.get_hand import hands


start_time = None

def landmark_distance(landmarkAx, landmarkAy, landmarkBx, landmarkBy):
    return math.sqrt((landmarkAx - landmarkBx) ** 2 + (landmarkAy - landmarkBy) ** 2)

def right_click(thumbX, thumbY, pinkyX, pinkyY, touching_threshold = 0.15, holding_time=0.2):

    global start_time
    distance = landmark_distance(thumbX, thumbY, pinkyX, pinkyY)

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

def left_click(thumbX, thumbY, ringX, ringY, touching_threshold = 0.15, holding_time=0.2):

    global start_time
    distance = landmark_distance(thumbX, thumbY, ringX, ringY)

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

def double_click(thumbX, thumbY, middleX, middleY, touching_threshold = 0.15, holding_time=0.2):

    global start_time
    distance = landmark_distance(thumbX, thumbY, middleX, middleY)

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