import ctypes

class PressKeys:

    KEYEVENTF_EXTENDEDKEY = 0x0001
    KEYEVENTF_KEYUP = 0x0002

    @staticmethod
    def press_key(hexKeyCode):
        ctypes.windll.user32.keybd_event(hexKeyCode, 0, PressKeys.KEYEVENTF_EXTENDEDKEY, 0)
    @staticmethod
    def release_key(hexKeyCode):
        ctypes.windll.user32.keybd_event(hexKeyCode, 0, PressKeys.KEYEVENTF_EXTENDEDKEY | PressKeys.KEYEVENTF_KEYUP, 0)
