from pynput.mouse import Controller
import subprocess


position_history = []
past_positions_max_amount = 5
mouse = Controller()

#getting screen size
def get_screen_size():
    try:
        result = subprocess.run(['xrandr'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if '*' in line:
                resolution = line.split()[0]
                width, height = map(int, resolution.split('x'))
                return width, height
    except:
        pass
    return 1920, 1080 

def move_cursor(webcam_x, webcam_y):
    """
    Simple cursor control - maps webcam to screen using pynput

        webcam_x (int): X coordinate in webcam (0-640)
        webcam_y (int): Y coordinate in webcam (0-480)
    """

    screen_width, screen_height = get_screen_size()
    
    screen_x = int(((640 - webcam_x) / 640) * screen_width)
    screen_y = int((webcam_y / 480) * screen_height)
    

    position_history.append((screen_x, screen_y))
    
    if len(position_history) > past_positions_max_amount:
        position_history.pop(0)

    avg_x = sum(pos[0] for pos in position_history) / len(position_history)
    avg_y = sum(pos[1] for pos in position_history) / len(position_history)
    
    mouse.position = (int(avg_x), int(avg_y))
