import math
import time
from pynput.mouse import Button, Controller
import lefthand_actions

mouse = Controller()
last_click_time = 0
click_delay = 0.5
default_threshold = 0.05
ok_used = False


def landmark_distance(landmarkAx, landmarkAy, landmarkBx, landmarkBy):
    return math.sqrt((landmarkAx - landmarkBx) ** 2 + (landmarkAy - landmarkBy) ** 2)


def scale_threshold(wristX, wristY, middleX, middleY, threshold=default_threshold):
    distance_wrist_to_middle = landmark_distance(wristX, wristY, middleX, middleY)

    reference_distance = 0.4  # default distance from wrist to middle finger is 0.4
    scaled_threshold = threshold * (distance_wrist_to_middle / reference_distance)

    return scaled_threshold


def right_click(thumbX, thumbY, pinkyX, pinkyY, touching_threshold=default_threshold, holding_time=0.2):
    global last_click_time
    distance = landmark_distance(thumbX, thumbY, pinkyX, pinkyY)

    if lefthand_actions.is_left_hand_dragging():
        return False

    if distance <= touching_threshold:
        current_time = time.time()
        if current_time - last_click_time >= click_delay:
            mouse.click(Button.right, 1)
            last_click_time = current_time
            return True
    return False


def left_click(thumbX, thumbY, ringX, ringY, touching_threshold=default_threshold, holding_time=0.2):
    global last_click_time
    distance = landmark_distance(thumbX, thumbY, ringX, ringY)

    if lefthand_actions.is_left_hand_dragging():
        return False

    if distance <= touching_threshold:
        current_time = time.time()
        if current_time - last_click_time >= click_delay:
            mouse.click(Button.left, 1)
            last_click_time = current_time
            lefthand_actions.set_right_hand_left_click_status(True)
            return True
    else:
        lefthand_actions.set_right_hand_left_click_status(False)
    return False


def double_click(thumbX, thumbY, middleX, middleY, touching_threshold=default_threshold, holding_time=0.2):
    global last_click_time
    distance = landmark_distance(thumbX, thumbY, middleX, middleY)

    if lefthand_actions.is_left_hand_dragging() | lefthand_actions.is_left_hand_scrolling():  # Disable clicks when left hand is dragging
        return False

    if distance <= touching_threshold:
        current_time = time.time()
        if current_time - last_click_time >= click_delay:
            mouse.click(Button.left, 1)
            time.sleep(0.2)
            mouse.click(Button.left, 1)
            last_click_time = current_time
            return True
    return False


ok_hold_start = None


def ok_symbol(thumbX, thumbY, indexX, indexY, touching_threshold=default_threshold, holding_time=1.0):
    global last_click_time, ok_used, ok_hold_start
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
        lefthand_actions.set_right_hand_left_click_status(False)
    return False