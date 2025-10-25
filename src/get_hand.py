import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Create hands solution
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def process_hand_frame(frame):
    """
    Process a frame to detect hand landmarks
    
    Args:
        frame: Input frame from webcam
        
    Returns:
        tuple: (annotated_frame, landmarks_list)
    """
    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame
    results = hands.process(rgb_frame)
    
    # Create annotated frame
    annotated_frame = frame.copy()
    
    landmarks_list = []
    
    # Draw hand landmarks if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(
                annotated_frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
            
            # Store landmarks for movement tracking
            landmarks_list.append(hand_landmarks.landmark)
    
    return annotated_frame, landmarks_list

def get_hand_position(landmarks, frame_shape):
    """
    Get hand center position from landmarks
    
    Args:
        landmarks: MediaPipe hand landmarks
        frame_shape: Shape of the frame (height, width, channels)
        
    Returns:
        tuple: (x, y) coordinates of hand center
    """
    if not landmarks:
        return None, None
    
    # Get wrist position (landmark 0)
    wrist = landmarks[0]
    height, width = frame_shape[:2]
    
    x = int(wrist.x * width)
    y = int(wrist.y * height)
    
    return x, y

def cleanup_hands():
    """Release MediaPipe resources"""
    hands.close()
