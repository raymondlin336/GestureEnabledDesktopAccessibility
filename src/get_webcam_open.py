import cv2
import numpy as np
import get_hand
import time
from cursor_control import move_cursor
from mouse_actions import right_click, left_click, double_click, landmark_distance

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  
cap.set(cv2.CAP_PROP_FPS, 60)


if not cap.isOpened():
    print("Error: Webcam could not be opened")
    exit()
else:
    print("Webcam initialized!")
    print(f"Frame size: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    print(f"FPS: {cap.get(cv2.CAP_PROP_FPS)}")

while True:

    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame from webcam")
        break
    
    

    annotated_frame, landmarks, handedness = get_hand.process_hand_frame(frame)

    # Index 8 of right hand (index finger tip) 
    if landmarks and handedness:
        for i, (hand_landmarks, hand_type) in enumerate(zip(landmarks, handedness)):
            if hand_type == "Left":
                index_tip = hand_landmarks[8]
                thumb_tip = hand_landmarks[4]
                middle_tip = hand_landmarks[12]
                ring_tip = hand_landmarks[16]
                pinky_tip = hand_landmarks[20]
                wrist = hand_landmarks[0]
                
                pixel_x = int(index_tip.x * frame.shape[1])
                pixel_y = int(index_tip.y * frame.shape[0])
                
                move_cursor(pixel_x, pixel_y)
                print(landmark_distance(wrist.x, wrist.y, middle_tip.x, middle_tip.y))
                if right_click(thumb_tip.x, thumb_tip.y, pinky_tip.x, pinky_tip.y):
                    pass
                if left_click(thumb_tip.x, thumb_tip.y, ring_tip.x, ring_tip.y):
                    pass
                if double_click(thumb_tip.x, thumb_tip.y, middle_tip.x, middle_tip.y):
                    pass
                
                cv2.circle(annotated_frame, (pixel_x, pixel_y), 10, (0, 255, 0), -1)
                break


    inverted_frame = cv2.flip(annotated_frame, 1)
    cv2.imshow('Hand Tracking', inverted_frame)

  
    if cv2.waitKey(1) & 0xFF == ord('q'): #exit with q key
        break

cap.release()
get_hand.cleanup_hands() 
cv2.destroyAllWindows()
