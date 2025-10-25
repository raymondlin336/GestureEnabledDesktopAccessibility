import json
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


class GesturePanel(tk.Tk):
    def __init__(self, gestures, default_actions, config_path: str):
        super().__init__()
        self.title("Gesture Key Mapper")
        self.geometry("560x360")
        self.minsize(520, 360)

        self.gestures = list(gestures)
        self.defaults = dict(default_actions)
        self.config_path = config_path

        self.vars: dict[str, tk.StringVar] = {}

        # Precompute the choices from the dict KEYS
        # (sorted for nicer UX; remove sorted() if you want original insertion order)
        self.choices = [""] + sorted(list(Common_Actions.keys()))

        # Main Layout
        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        header = ttk.Label(container, text="Map Gestures to Key Inputs / Actions",
                           font=("TkDefaultFont", 11, "bold"))
        header.pack(anchor="w", pady=(0, 8))

        # Table
        table = ttk.Frame(container)
        table.pack(fill="both", expand=True)

        ttk.Label(table, text="Gesture", font=("TkDefaultFont", 10, "bold")).grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 6)
        )
        ttk.Label(table, text="Key / Action", font=("TkDefaultFont", 10, "bold")).grid(
            row=0, column=1, sticky="w"
        )

        # Rows
        for r, g in enumerate(self.gestures, start=1):
            ttk.Label(table, text=g).grid(row=r, column=0, sticky="w", padx=(0, 8), pady=4)

            sv = tk.StringVar(value=self.defaults.get(g, ""))
            self.vars[g] = sv

            row_frame = ttk.Frame(table)
            row_frame.grid(row=r, column=1, sticky="ew", pady=4)
            table.grid_columnconfigure(1, weight=1)
            row_frame.grid_columnconfigure(0, weight=1)

            # Combobox
            combo = ttk.Combobox(row_frame, values=self.choices, state="readonly", textvariable=sv)
            combo.grid(row=0, column=0, sticky="ew")

            # Make sure default is actually one of the keys (or blank)
            default_val = self.defaults.get(g, "")
            combo.set(default_val if default_val in self.choices else "")

            combo.bind("<<ComboboxSelected>>",
                       lambda e, gest=g, cb=combo: self._apply_common_action(gest, cb.get()))

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

    def get_mapping(self) -> dict[str, str]:
        """Return gesture -> selected action NAME (key in Common_Actions)."""
        result = {}
        for gesture in self.gestures:
            value = self.vars[gesture].get()
            value = value.strip() if isinstance(value, str) else str(value).strip()
            result[gesture] = value
        return result

    def get_resolved_mapping(self) -> dict[str, object]:
        """
        Return gesture -> resolved code(s) from Common_Actions.
        Values can be a string like '0xAF' or a list like ['0x5B','0xA2','0x25'].
        Unknown/blank actions map to ''.
        """
        names = self.get_mapping()
        return {g: Common_Actions.get(name, "") for g, name in names.items()}

    def reset_to_defaults(self):
        for g in self.gestures:
            dv = self.defaults.get(g, "")
            self.vars[g].set(dv if dv in self.choices else "")

    def save_config(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.get_mapping(), f, indent=2)
            messagebox.showinfo("Saved", f"Saved to:\n{self.config_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_config(self):
        try:
            p = Path(self.config_path)
            if not p.exists():
                messagebox.showwarning("Missing", f"No file at:\n{p}")
                return
            data = json.load(open(p, "r", encoding="utf-8"))
            for g, v in data.items():
                if g in self.vars:
                    self.vars[g].set(v if v in self.choices else "")
            messagebox.showinfo("Loaded", f"Loaded from:\n{p}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def finish_and_close(self):
        print("Selected (names):", self.get_mapping())
        print("Selected (codes):", self.get_resolved_mapping())
        self.destroy()




if __name__ == "__main__":
    #Preset variables
    Gestures = [
        "fist",
        "thumbs_up",
        "thumps_down",
        "swipe_right",
        "swipe_left",
    ]

    Common_Actions = {
        "volume_up" : "0xAF",
        "volume_down" : "0xAE",
        "mute_toggle" : "0xAD",
        "play_pause" : "0xB3",
        "next_track" : "0xB0",
        "prev_track" : "0xB1",
        "switch_to_right_desktop" : ["0x5B", "0xA2", "0x25"],
        "switch_to_left_desktop" : ["0x5B", "0xA2", "0x27"],
    }

    #Find path next to this file
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config.json"

    if not config_path.exists():
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(Default_Actions, f, indent=2)
        print(f"Created new config file at {config_path}")

    app = GesturePanel(Gestures, Default_Actions, str(config_path))
    app.mainloop()