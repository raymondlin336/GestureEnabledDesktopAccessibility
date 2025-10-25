import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2)
img = cv2.imread("hand_sample.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
result = hands.process(img_rgb)

if result.multi_hand_landmarks:
    for hand in result.multi_hand_landmarks:
        mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
cv2.imshow("Hand Detection", img)
cv2.waitKey(0)
