import cv2
import mediapipe as mp
import get_hand
from src.get_hand import hands
from src.get_webcam_open import landmarks

if hands:
    for hand in hands:
        for id in