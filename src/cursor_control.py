from pynput.mouse import Controller
import subprocess


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
    Uses pynput library to control a cursor which takes the coordinates of index 8 of the right hand (right index fingertip)
    webcam_x -> (int)
    webcam_y -> (int)
    """

    screen_width, screen_height = get_screen_size()
    screen_x = int(screen_width - ((webcam_x / 640) * screen_width))
    screen_y = int((webcam_y / 480) * screen_height)
    mouse = Controller()
    mouse.position = (screen_x, screen_y)
