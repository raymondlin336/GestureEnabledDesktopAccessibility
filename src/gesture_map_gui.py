import json
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path


Default_Config_Path = "../gesture_map_config.json"

Gestures = [
    "Palm Open",
    "Palm Closed",
    "Thumbs Up",
    "Thumbs Down",
]

Default_Actions = {
    "Thumbs Up": "volume_up",
    "Thumbs Down": "volume_down",
    "Palm Open": "",
    "Palm Closed": "",
}

Common_Actions = [
    "volume_up",
    "volume_down",
    "mute_toggle",
    "play_pause",
    "next_track",
    "prev_track",
    "task_manager",
    "brightness_up",
    "brightness_down",
    "screenshot",
    "custom:ctrl+alt+T",
]

class GesturePanel(tk.Tk):
    def __init__(self, gestures, default_actions, config_path : str):
        super().__init__()
        self.title("Gesture Key Mapper")
        self.geometry("560x360")
        self.minsize(520, 360)

        self.gestures = list(gestures)
        self.defaults = dict(default_actions)
        self.config_path = config_path

        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        header = ttk.Label(container, text="Map Gestures to Key Inputs / Actions", font=("TkDefaultFont", 10, "bold"))
        header.pack(anchor="w", pady=(0, 8))


if __name__ == "__main__":
    app = GesturePanel(Gestures, Default_Actions, Default_Config_Path)
    app.mainloop()