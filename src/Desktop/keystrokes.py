import ctypes

# Reference: https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes

class PressKeys:
    VK_VOLUME_MUTE = 0xAD
    VK_VOLUME_DOWN = 0xAE
    VK_VOLUME_UP = 0xAF
    VK_MEDIA_NEXT_TRACK = 0xB0
    VK_MEDIA_PREV_TRACK = 0xB1
    VK_MEDIA_PLAY_PAUSE = 0xB3

    # SendInput key event types
    KEYEVENTF_EXTENDEDKEY = 0x0001
    KEYEVENTF_KEYUP = 0x0002

    @staticmethod
    def press_key(hexKeyCode):
        print(hexKeyCode)
        """Simulate pressing a single key by virtual key code."""
        ctypes.windll.user32.keybd_event(hexKeyCode, 0, PressKeys.KEYEVENTF_EXTENDEDKEY, 0)
        ctypes.windll.user32.keybd_event(hexKeyCode, 0, PressKeys.KEYEVENTF_EXTENDEDKEY | PressKeys.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def volume_up():
        PressKeys.press_key(PressKeys.VK_VOLUME_UP)

    @staticmethod
    def volume_down():
        PressKeys.press_key(PressKeys.VK_VOLUME_DOWN)

    @staticmethod
    def mute():
        PressKeys.press_key(PressKeys.VK_VOLUME_MUTE)

    @staticmethod
    def play_pause():
        PressKeys.press_key(PressKeys.VK_MEDIA_PLAY_PAUSE)


if __name__ == "__main__":
    PressKeys.volume_up()        # Increase system volume
    # volume_down()      # Decrease system volume
    # mute()             # Toggle mute
    # play_pause()       # Play / pause media
    # next_track()       # Skip to next track
    # previous_track()   # Go to previous track
