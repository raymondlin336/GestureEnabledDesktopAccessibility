import cv2
import numpy as np
import gui_hands
import time
from cursor_control import move_cursor
import gui_hands_mapping
from gui_hands_mapping import ok_symbol, ok2_symbol, ok3_symbol, scale_threshold
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path



def run_selector_program() -> str:
    base_dir = Path(__file__).resolve().parent
    return_val = "cp"
    gui_hands_mapping.ok_used = False
    root = tk.Tk()
    root.title("Selector Mode:")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    closed_by_user = {"flag": False}

    def _on_close():
        closed_by_user["flag"] = True
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", _on_close)

    # frame layout:
    frame_main = tk.Frame(root, bg="black")
    frame_main.pack(padx=6, pady=6)

    #load image
    try:
        img_path = Path(__file__).resolve().parent / "selector_img.jpg"
        static_img = Image.open(img_path)
        static_img = static_img.resize((856, 480))
        static_img_tk = ImageTk.PhotoImage(static_img)
        label_static = tk.Label(frame_main, image=static_img_tk)
        label_static.image = static_img_tk
        label_static.grid(row=0, column=0, padx=5)
    except Exception as e:
        label_static = tk.Label(frame_main, text="(Image not found)", fg="red")
        label_static.grid(row=0, column=0, padx=5)

    cam_label = tk.Label(frame_main)
    cam_label.grid(row=0, column=1, padx=5)

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 60)

    if not cap.isOpened():
        print("Error: Webcam could not be opened")
        root.destroy()
        exit()
    else:
        print("Webcam initialized!")
        print(f"Frame size: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
        print(f"FPS: {cap.get(cv2.CAP_PROP_FPS)}")

    while True:

        if closed_by_user["flag"]:
            return_val = "quit"
            print("Selector window closed by user.")
            break
        root.update_idletasks()
        root.update()

        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame from webcam")
            break

        annotated_frame, landmarks, handedness = gui_hands.process_hand_frame(frame)

        gesture_detected = False

        if landmarks and handedness:

            for i, (hand_landmarks, hand_type) in enumerate(zip(landmarks, handedness)):
                    index_tip = hand_landmarks[8]
                    thumb_tip = hand_landmarks[4]
                    middle_tip = hand_landmarks[12]
                    ring_tip = hand_landmarks[16]
                    pinky_tip = hand_landmarks[20]
                    wrist = hand_landmarks[0]

                    scaled_threshold = scale_threshold(wrist.x, wrist.y, middle_tip.x, middle_tip.y)

                    if ok_symbol(thumb_tip.x, thumb_tip.y, index_tip.x, index_tip.y, scaled_threshold,
                                     holding_time=0.5):
                        print("OK gesture detected")
                        return_val = "quit"
                        gesture_detected = True
                        break

                    if ok2_symbol(thumb_tip.x, thumb_tip.y, middle_tip.x, middle_tip.y, scaled_threshold,
                                      holding_time=0.5):
                        print("OK2 gesture detected")
                        return_val = "gp"
                        gesture_detected = True
                        break

                    if ok3_symbol(thumb_tip.x, thumb_tip.y, ring_tip.x, ring_tip.y, scaled_threshold,
                                      holding_time=0.5):
                        print("OK3 gesture detected")
                        return_val = "cp"
                        gesture_detected = True
                        break

        inverted_frame = cv2.flip(annotated_frame, 1)
        frame_rgb = cv2.cvtColor(inverted_frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        cam_label.configure(image=img_tk)
        cam_label.image = img_tk

        #

        if gesture_detected:
            print("Quitting GUI Mode")
            break

    cap.release()
    gui_hands.cleanup_hands()
    cv2.destroyAllWindows()

    try:
        if root.winfo_exists():
            root.destroy()
    except tk.TclError:
        pass

    return return_val


if __name__ == "__main__":
    k = run_selector_program()
    print(k)
