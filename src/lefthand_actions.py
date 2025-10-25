import math
import time
from pynput.mouse import Button, Controller

mouse = Controller()
is_dragging = False
right_hand_left_click_active = False
default_threshold = 0.15

def landmark_distance(landmarkAx, landmarkAy, landmarkBx, landmarkBy):
    return math.sqrt((landmarkAx - landmarkBx) ** 2 + (landmarkAy - landmarkBy) ** 2)

def left_scale_threshold(wristX, wristY, middleX, middleY, threshold = default_threshold):
    distance_wrist_to_middle = landmark_distance(wristX, wristY, middleX, middleY)

    reference_distance = 0.4  # default distance from wrist to middle finger is 0.4
    scaled_threshold = threshold * (distance_wrist_to_middle / reference_distance)

    return scaled_threshold
def all_fingers_distance(landmarkAx, landmarkAy, landmarkBx, landmarkBy, landmarkCx, landmarkCy, landmarkDx, landmarkDy, landmarkEx, landmarkEy):
    points = [(landmarkAx, landmarkAy), (landmarkBx, landmarkBy), (landmarkCx, landmarkCy), (landmarkDx, landmarkDy), (landmarkEx, landmarkEy)]
    distance = 0

    for i in range(len(points)):
        for j in range(i+1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]
            distance += math.sqrt((x1-x2)**2 + (y1-y2)**2)

    return distance

def set_right_hand_left_click_status(status):
    global right_hand_left_click_active
    right_hand_left_click_active = status

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

def left_hand_drag(landmarks):
    global is_dragging, right_hand_left_click_active
    
    is_fist = detect_fist(landmarks)
    
    if is_fist:
        if not is_dragging:
            mouse.press(Button.left)
            is_dragging = True
        return True
    else:
        if is_dragging:
            mouse.release(Button.left)
            is_dragging = False
        return False

def is_left_hand_dragging():
    return is_dragging