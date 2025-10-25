import cv2
import numpy as np
import get_hand
import time
from cursor_control import move_cursor

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

    # Index 8 of right hand (index finger tip) to control the mouse
    if landmarks and handedness:
        for i, (hand_landmarks, hand_type) in enumerate(zip(landmarks, handedness)):
            if hand_type == "Left":  # "Left" is actually right hand since the webcam is inverted
                index_tip = hand_landmarks[8]

                pixel_x = int(index_tip.x * frame.shape[1])
                pixel_y = int(index_tip.y * frame.shape[0])

                move_cursor(pixel_x, pixel_y)
                cv2.circle(annotated_frame, (pixel_x, pixel_y), 10, (0, 255, 0), -1) #highlights the right index tip


                print(f"Right hand index finger tip: ({pixel_x}, {pixel_y})")
                break


    inverted_frame = cv2.flip(annotated_frame, 1)
    cv2.imshow('Hand Tracking', inverted_frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
get_hand.cleanup_hands()
cv2.destroyAllWindows()
