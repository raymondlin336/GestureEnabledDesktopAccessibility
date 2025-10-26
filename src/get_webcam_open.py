import cv2
import numpy as np
import get_hand
import time
from cursor_control import move_cursor
import righthand_actions
from righthand_actions import right_click, left_click, double_click, scale_threshold, landmark_distance
from lefthand_actions import left_hand_drag, left_scale_threshold, left_hand_scroll, is_left_hand_scrolling
from righthand_actions import ok_symbol

def run_cursor_program():
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

        if landmarks and handedness:
            for i, (hand_landmarks, hand_type) in enumerate(zip(landmarks, handedness)):
                if hand_type == "Left": #"left" is right hand in real life (inverted webcam)
                    index_tip = hand_landmarks[8]
                    thumb_tip = hand_landmarks[4]
                    middle_tip = hand_landmarks[12]
                    ring_tip = hand_landmarks[16]
                    pinky_tip = hand_landmarks[20]
                    wrist = hand_landmarks[0]

                    pixel_x = int(index_tip.x * frame.shape[1])
                    pixel_y = int(index_tip.y * frame.shape[0])

                    move_cursor(pixel_x, pixel_y)

                    scaled_threshold = scale_threshold(wrist.x, wrist.y, middle_tip.x, middle_tip.y)


                    if right_click(thumb_tip.x, thumb_tip.y, pinky_tip.x, pinky_tip.y, scaled_threshold):
                        pass
                    if left_click(thumb_tip.x, thumb_tip.y, ring_tip.x, ring_tip.y, scaled_threshold):
                        pass
                    if double_click(thumb_tip.x, thumb_tip.y, middle_tip.x, middle_tip.y, scaled_threshold):
                        pass
                    ok_symbol(thumb_tip.x, thumb_tip.y, index_tip.x, index_tip.y, scaled_threshold)

                    cv2.circle(annotated_frame, (pixel_x, pixel_y), 10, (0, 255, 0), -1)

                elif hand_type == "Right": #"right" is left hand in real life (inverted webcam)

                    index_tip = hand_landmarks[8]
                    thumb_tip = hand_landmarks[4]
                    middle_tip = hand_landmarks[12]
                    ring_tip = hand_landmarks[16]
                    pinky_tip = hand_landmarks[20]
                    wrist = hand_landmarks[0]

                    pixel_x = int(index_tip.x * frame.shape[1])
                    pixel_y = int(index_tip.y * frame.shape[0])

                    left_hand_drag(hand_landmarks)
                    left_hand_scroll(hand_landmarks, frame.shape[0])

                    scaled_threshold = scale_threshold(wrist.x, wrist.y, middle_tip.x, middle_tip.y)
                    ok_symbol(thumb_tip.x, thumb_tip.y, index_tip.x, index_tip.y, scaled_threshold)

                    #left hand visuals
                    if is_left_hand_scrolling():
                        cv2.circle(annotated_frame, (pixel_x, pixel_y), 15, (0, 0, 255), -1)
                    else:
                        cv2.circle(annotated_frame, (pixel_x, pixel_y), 10, (255, 0, 0), -1)


        inverted_frame = cv2.flip(annotated_frame, 1) #invert cam
        cv2.imshow('Hand Tracking', inverted_frame)

        if cv2.waitKey(1) & righthand_actions.ok_used:
            print("Quitting Cursor Mode")
            break

    cap.release()
    get_hand.cleanup_hands()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_cursor_program()
