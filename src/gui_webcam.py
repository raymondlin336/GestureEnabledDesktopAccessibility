import cv2
import numpy as np
import gui_hands
import time
from cursor_control import move_cursor
import gui_hands_mapping
from gui_hands_mapping import ok_symbol as gui_ok_symbol, fist_symbol, palm_symbol, detect_fist, detect_palm, scale_threshold


def run_gui_program():
    gui_hands_mapping.ok_used = False
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

        annotated_frame, landmarks, handedness = gui_hands.process_hand_frame(frame)

        if landmarks and handedness:
            for i, (hand_landmarks, hand_type) in enumerate(zip(landmarks, handedness)):
                if hand_type == "Left":  # "left" is right hand in real life (inverted webcam)
                    index_tip = hand_landmarks[8]
                    thumb_tip = hand_landmarks[4]
                    middle_tip = hand_landmarks[12]
                    ring_tip = hand_landmarks[16]
                    pinky_tip = hand_landmarks[20]
                    wrist = hand_landmarks[0]

                    scaled_threshold = scale_threshold(wrist.x, wrist.y, middle_tip.x, middle_tip.y)
                    
                   
                    if gui_ok_symbol(thumb_tip.x, thumb_tip.y, index_tip.x, index_tip.y, scaled_threshold, holding_time=0.5):
                        print("OK gesture detected")
                        break
                
                    if detect_fist(hand_landmarks):
                        if fist_symbol(thumb_tip.x, thumb_tip.y, index_tip.x, index_tip.y, scaled_threshold, holding_time=0.5):
                            print("Fist gesture detected")
                            break
                    
                    if detect_palm(hand_landmarks):
                        if palm_symbol(thumb_tip.x, thumb_tip.y, index_tip.x, index_tip.y, scaled_threshold, holding_time=0.5):
                            print("Palm up gesture detected")
                            break

                elif hand_type == "Right":  # "right" is left hand in real life (inverted webcam)
                    index_tip = hand_landmarks[8]
                    thumb_tip = hand_landmarks[4]
                    middle_tip = hand_landmarks[12]
                    ring_tip = hand_landmarks[16]
                    pinky_tip = hand_landmarks[20]
                    wrist = hand_landmarks[0]

                    scaled_threshold = scale_threshold(wrist.x, wrist.y, middle_tip.x, middle_tip.y)               
                 
                    if gui_ok_symbol(thumb_tip.x, thumb_tip.y, index_tip.x, index_tip.y, scaled_threshold, holding_time=0.5):
                        print("OK gesture detected")
                        break
                
                    if detect_fist(hand_landmarks):
                        if fist_symbol(thumb_tip.x, thumb_tip.y, index_tip.x, index_tip.y, scaled_threshold, holding_time=0.5):
                            print("Fist gesture detected")
                            break
             
                    if detect_palm(hand_landmarks):
                        if palm_symbol(thumb_tip.x, thumb_tip.y, index_tip.x, index_tip.y, scaled_threshold, holding_time=0.5):
                            print("Palm up gesture detected")
                            break


        inverted_frame = cv2.flip(annotated_frame, 1)  # invert cam
        cv2.imshow('GUI', inverted_frame)

        cv2.waitKey(1)

        if gui_hands_mapping.ok_used:
            print("Quitting GUI Mode")
            break

    cap.release()
    gui_hands.cleanup_hands()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_gui_program()
