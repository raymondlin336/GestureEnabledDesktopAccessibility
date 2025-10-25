import math
import time
from pynput.mouse import Button, Controller

mouse = Controller()
last_click_time = 0
click_delay = 0.5
default_threshold = 0.05 #try to scale the threshold to the distance of the hand from the screen (landmark 0 and 12)


def landmark_distance(landmarkAx, landmarkAy, landmarkBx, landmarkBy):
    return math.sqrt((landmarkAx - landmarkBx) ** 2 + (landmarkAy - landmarkBy) ** 2)

def scale_threshold(wristX, wristY, middleX, middleY, threshold = default_threshold):
    distance_wrist_to_middle = landmark_distance(wristX, wristY, middleX, middleY)

    reference_distance = 0.4 #default distance from wrist to middle finger is 0.4
    scaled_threshold = threshold * (distance_wrist_to_middle / reference_distance)
    
    return scaled_threshold



def right_click(thumbX, thumbY, pinkyX, pinkyY, touching_threshold = default_threshold, holding_time=0.2):
    global last_click_time
    distance = landmark_distance(thumbX, thumbY, pinkyX, pinkyY)

    if distance <= touching_threshold:
        current_time = time.time()
        if current_time - last_click_time >= click_delay:
            mouse.click(Button.right, 1)
            last_click_time = current_time
            return True
    return False

def left_click(thumbX, thumbY, ringX, ringY, touching_threshold = default_threshold, holding_time=0.2):
    global last_click_time
    distance = landmark_distance(thumbX, thumbY, ringX, ringY)

    if distance <= touching_threshold:
        current_time = time.time()
        if current_time - last_click_time >= click_delay:
            mouse.click(Button.left, 1)
            last_click_time = current_time
            return True
    return False

def double_click(thumbX, thumbY, middleX, middleY, touching_threshold = default_threshold, holding_time=0.2):
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