import pyautogui

def move_cursor(webcam_x, webcam_y):
    """
    Simple cursor control - maps webcam to screen
    
    Args:
        webcam_x (int): X coordinate in webcam (0-640)
        webcam_y (int): Y coordinate in webcam (0-480)
    """

    screen_width, screen_height = pyautogui.size()

    screen_x = int((webcam_x / 640) * screen_width)
    screen_y = int((webcam_y / 480) * screen_height)

    pyautogui.moveTo(screen_x, screen_y)
