import math
import time
from pynput.mouse import Button, Controller


mouse = Controller()

default_threshold = 0.05
ok_used = False


def landmark_distance(landmarkAx, landmarkAy, landmarkBx, landmarkBy):
    return math.sqrt((landmarkAx - landmarkBx) ** 2 + (landmarkAy - landmarkBy) ** 2)


def scale_threshold(wristX, wristY, middleX, middleY, threshold=default_threshold):
    distance_wrist_to_middle = landmark_distance(wristX, wristY, middleX, middleY)

    reference_distance = 0.4  # default distance from wrist to middle finger is 0.4
    scaled_threshold = threshold * (distance_wrist_to_middle / reference_distance)

    return scaled_threshold

hold_fist_start = None


def fist_symbol(thumbX, thumbY, indexX, indexY, touching_threshold=default_threshold, holding_time=1.0):
    global ok_used, hold_fist_start
    distance = landmark_distance(thumbX, thumbY, indexX, indexY)

    if distance <= touching_threshold:
        current_time = time.time()

        if hold_fist_start is None:
            hold_fist_start = current_time

        hold_duration = current_time - hold_fist_start
        if hold_duration >= holding_time:
            print("detected fist - quitting")
            ok_used = True
            return True
    else:

        hold_fist_start = None

    return False

palm_up_start = None


def palm_symbol(thumbX, thumbY, indexX, indexY, touching_threshold=default_threshold, holding_time=1.0):
    global ok_used, palm_up_start
    distance = landmark_distance(thumbX, thumbY, indexX, indexY)

    if distance <= touching_threshold:
        current_time = time.time()

        if palm_up_start is None:
            palm_up_start = current_time

        hold_duration = current_time - palm_up_start
        if hold_duration >= holding_time:
            print("detected palm - quitting")
            ok_used = True
            return True
    else:

        palm_up_start = None

    return False

ok_hold_start = None


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


def detect_fist(landmarks):

    if not landmarks:
        return False


    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]


    thumb_mcp = landmarks[3]
    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    pinky_mcp = landmarks[17]


    fingers_down = []
    fingers_down.append(thumb_tip.x < thumb_mcp.x)
    fingers_down.append(index_tip.y > index_mcp.y)
    fingers_down.append(middle_tip.y > middle_mcp.y)
    fingers_down.append(ring_tip.y > ring_mcp.y)
    fingers_down.append(pinky_tip.y > pinky_mcp.y)

    return sum(fingers_down) >= 4

def is_fist():
    return is_fist

def detect_palm(landmarks):

    if not landmarks:
        return False


    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]


    thumb_mcp = landmarks[3]
    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    pinky_mcp = landmarks[17]


    fingers_down = []
    fingers_down.append(thumb_tip.x < thumb_mcp.x)
    fingers_down.append(index_tip.y > index_mcp.y)
    fingers_down.append(middle_tip.y > middle_mcp.y)
    fingers_down.append(ring_tip.y > ring_mcp.y)
    fingers_down.append(pinky_tip.y > pinky_mcp.y)

    return sum(fingers_down) == 0

def is_palm():
    return is_palm