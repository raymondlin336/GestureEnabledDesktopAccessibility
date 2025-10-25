import math
import time
from pynput.mouse import Button, Controller

mouse = Controller()
last_click_time = 0
click_delay = 0.5
threshold = 0.01


def landmark_distance(landmarkAx, landmarkAy, landmarkBx, landmarkBy):
    return math.sqrt((landmarkAx - landmarkBx) ** 2 + (landmarkAy - landmarkBy) ** 2)

def right_click(thumbX, thumbY, pinkyX, pinkyY, touching_threshold = threshold, holding_time=0.2):
    global last_click_time
    distance = landmark_distance(thumbX, thumbY, pinkyX, pinkyY)

    if distance <= touching_threshold:
        current_time = time.time()
        if current_time - last_click_time >= click_delay:
            mouse.click(Button.right, 1)
            last_click_time = current_time
            return True
    return False

def left_click(thumbX, thumbY, ringX, ringY, touching_threshold = threshold, holding_time=0.2):
    global last_click_time
    distance = landmark_distance(thumbX, thumbY, ringX, ringY)

    if distance <= touching_threshold:
        current_time = time.time()
        if current_time - last_click_time >= click_delay:
            mouse.click(Button.left, 1)
            last_click_time = current_time
            return True
    return False

def double_click(thumbX, thumbY, middleX, middleY, touching_threshold = threshold, holding_time=0.2):
    global last_click_time
    distance = landmark_distance(thumbX, thumbY, middleX, middleY)

    if distance <= touching_threshold:
        current_time = time.time()
        if current_time - last_click_time >= click_delay:
            mouse.click(Button.left, 1)
            time.sleep(0.2)
            mouse.click(Button.left, 1)
            last_click_time = current_time
            return True
    return False