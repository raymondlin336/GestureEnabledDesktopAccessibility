import math
import time
from pynput.mouse import Button, Controller


mouse = Controller()

default_threshold = 0.05
ok_used = False
ok2_used = False
ok3_used = False


def landmark_distance(landmarkAx, landmarkAy, landmarkBx, landmarkBy):
    return math.sqrt((landmarkAx - landmarkBx) ** 2 + (landmarkAy - landmarkBy) ** 2)


def scale_threshold(wristX, wristY, middleX, middleY, threshold=default_threshold):
    distance_wrist_to_middle = landmark_distance(wristX, wristY, middleX, middleY)

    reference_distance = 0.4  # default distance from wrist to middle finger is 0.4
    scaled_threshold = threshold * (distance_wrist_to_middle / reference_distance)

    return scaled_threshold

ok_hold_start = None
ok2_hold_start = None
ok3_hold_start = None


def ok_symbol(thumbX, thumbY, indexX, indexY, touching_threshold=default_threshold, holding_time=1.0):
    global ok_used, ok_hold_start
    distance = landmark_distance(thumbX, thumbY, indexX, indexY)

    if distance <= touching_threshold:
        current_time = time.time()

        if ok_hold_start is None:
            ok_hold_start = current_time

        hold_duration = current_time - ok_hold_start
        if hold_duration >= holding_time:
            print("detected ok - quitting")
            ok_used = True
            return True
    else:

        ok_hold_start = None

    return False

def ok2_symbol(thumbX, thumbY, middleX, middleY, touching_threshold=default_threshold, holding_time=1.0):
    global ok2_used, ok2_hold_start
    distance = landmark_distance(thumbX, thumbY, middleX, middleY)

    if distance <= touching_threshold:
        current_time = time.time()

        if ok2_hold_start is None:
            ok2_hold_start = current_time

        hold_duration = current_time - ok2_hold_start
        if hold_duration >= holding_time:
            print("detected ok2 - quitting")
            ok2_used = True
            return True
    else:

        ok2_hold_start = None

    return False

def ok3_symbol(thumbX, thumbY, ringX, ringY, touching_threshold=default_threshold, holding_time=1.0):
    global ok3_used, ok3_hold_start
    distance = landmark_distance(thumbX, thumbY, ringX, ringY)

    if distance <= touching_threshold:
        current_time = time.time()

        if ok3_hold_start is None:
            ok3_hold_start = current_time

        hold_duration = current_time - ok3_hold_start
        if hold_duration >= holding_time:
            print("detected ok3 - quitting")
            ok3_used = True
            return True
    else:

        ok3_hold_start = None

    return False

