import cv2
import numpy as np
import get_hand


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
    
    

    annotated_frame, landmarks = get_hand.process_hand_frame(frame)

    #if landmarks:
        #for i, hand_landmarks in enumerate(landmarks):
            #x, y = get_hand.get_hand_position(hand_landmarks, frame.shape)
            #if x is not None:
                # Display hand position on frame
                #cv2.putText(annotated_frame, f"Hand {i+1}: ({x}, {y})",
                          #(10, 30 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    inverted_frame = cv2.flip(annotated_frame, 1)
    cv2.imshow('Hand Tracking', inverted_frame)

    # Exit on 'q' key press (you can replace this with hand gesture later)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
get_hand.cleanup_hands()  # Clean up MediaPipe resources
cv2.destroyAllWindows()
