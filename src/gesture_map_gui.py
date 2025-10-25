import json
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

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
            row_frame.grid(row=r, column=1, sticky="ew", pady=4)
            table.grid_columnconfigure(1, weight=1)
            row_frame.grid_columnconfigure(0, weight=1)

            # Combobox (read-only)
            combo = ttk.Combobox(row_frame, values=Common_Actions, state="readonly", textvariable=sv)
            combo.grid(row=0, column=0, sticky="ew")
            combo.set(self.defaults.get(g, "Choose…"))

            # When user picks a new value
            combo.bind("<<ComboboxSelected>>", lambda e, gest=g, cb=combo: self._apply_common_action(gest, cb.get()))

        # Buttons
        btns = ttk.Frame(container)
        btns.pack(fill="x", pady=(10, 0))

        save_btn = ttk.Button(btns, text="Save", command=self.save_config)
        load_btn = ttk.Button(btns, text="Load", command=self.load_config)
        reset_btn = ttk.Button(btns, text="Reset to Defaults", command=self.reset_to_defaults)
        start_btn = ttk.Button(btns, text="Start", command=self.finish_and_close)

        save_btn.pack(side="left")
        load_btn.pack(side="left", padx=6)
        reset_btn.pack(side="left")
        start_btn.pack(side="right")

    def _apply_common_action(self, gesture: str, val: str):
        if gesture in self.vars:
            self.vars[gesture].set(val)

    def get_mapping(self) -> dict[str,str]:
        """Return current gesture mapped to action mapping."""
        result = {}
        for gesture in self.gestures:
            value = self.vars[gesture].get()
            if isinstance(value, str):
                value = value.strip()
            else:
                value = str(value).strip()
            result[gesture] = value
        return result

    def reset_to_defaults(self):
        "Reset all values in gestures"
        for g in self.gestures:
            self.vars[g].set(self.defaults.get(g, ""))


if __name__ == "__main__":
    #Preset variables
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

    #Find path next to this file
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config.json"

    if not config_path.exists():
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(Default_Actions, f, indent=2)
        print(f"Created new config file at {config_path}")

    app = GesturePanel(Gestures, Default_Actions, str(config_path))
    app.mainloop()