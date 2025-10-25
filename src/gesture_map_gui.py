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

        self.vars: dict[str, tk.StringVar] = {}


        #Main Layout
        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        header = ttk.Label(container, text="Map Gestures to Key Inputs / Actions", font=("TkDefaultFont", 11, "bold"))
        header.pack(anchor="w", pady=(0, 8))

        #Table
        table = ttk.Frame(container)
        table.pack(fill="both", expand=True)

        ttk.Label(table, text="Gesture", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, sticky="w",
                                                                                  padx=(0, 8), pady=(0, 6))
        ttk.Label(table, text="Key / Action", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=1, sticky="w",)

        #Rows
        for r, g in enumerate(self.gestures, start=1):
            ttk.Label(table, text=g).grid(row=r, column=0, sticky="w", padx=(0, 8), pady=4)

            sv = tk.StringVar(value=self.defaults.get(g, ""))
            self.vars[g] = sv

            row_frame = ttk.Frame(table)
            # row_frame.grid(row=r, column=1, sticky="ew", pady=4)
            # table.grid_columnconfigure(1, weight=1)
            # row_frame.grid_columnconfigure(0, weight=1)

            entry = ttk.Entry(row_frame, textvariable=sv)
            entry.grid(row=0, column=0, sticky="ew")


            combo = ttk.Combobox(row_frame, values=Common_Actions, state="readonly")
            combo.set("Choose…")
            combo.grid(row=0, column=1, padx=6)
            combo.bind("<<ComboboxSelected>>", lambda e, gest=g, cb=combo: self._apply_common_action(gest, cb.get()))



if __name__ == "__main__":
    app = GesturePanel(Gestures, Default_Actions, Default_Config_Path)
    app.mainloop()