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

    # Index 8 of right hand (index finger tip) - CURSOR CONTROL
    if landmarks and handedness:
        for i, (hand_landmarks, hand_type) in enumerate(zip(landmarks, handedness)):
            if hand_type == "Left":  # This is your right hand
                index_tip = hand_landmarks[8]
                
                # Get webcam coordinates
                pixel_x = int(index_tip.x * frame.shape[1])
                pixel_y = int(index_tip.y * frame.shape[0])
                
                # Move cursor to screen coordinates
                move_cursor(pixel_x, pixel_y)
                
                # Draw circle on webcam frame
                cv2.circle(annotated_frame, (pixel_x, pixel_y), 10, (0, 255, 0), -1)
                
                # Display coordinates on frame
                cv2.putText(annotated_frame, f"Cursor: ({pixel_x}, {pixel_y})", 
                          (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                print(f"Right hand index finger tip: ({pixel_x}, {pixel_y})")
                break


    inverted_frame = cv2.flip(annotated_frame, 1)
    cv2.imshow('Hand Tracking', inverted_frame)

    # Exit on 'q' key press (you can replace this with hand gesture later)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
get_hand.cleanup_hands()  # Clean up MediaPipe resources
cv2.destroyAllWindows()
