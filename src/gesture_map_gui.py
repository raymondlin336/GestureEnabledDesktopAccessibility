import json
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

class GesturePanel(tk.Tk):
    def __init__(self, mappings_path: Path):
        super().__init__()
        self.title("Gesture Key Mapper")
        self.geometry("560x360")
        self.minsize(520, 360)

        self.mappings_path = mappings_path
        self.mappings_data = self._load_mappings(mappings_path)

        #build internal structures dicts and stuff
        self.gestures = [entry["gesture"] for entry in self.mappings_data]
        self.defaults = {entry["gesture"]: entry["function"] for entry in self.mappings_data}
        self.common_actions = {entry["function"]: entry["hexkey"] for entry in self.mappings_data}
        self.choices = sorted(list(self.common_actions.keys()))

        self.vars: dict[str, tk.StringVar] = {}

        # start ui
        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        header = ttk.Label(container, text="Map Gestures to Key Inputs / Actions",
                           font=("TkDefaultFont", 11, "bold"))
        header.pack(anchor="w", pady=(0, 8))

        table = ttk.Frame(container)
        table.pack(fill="both", expand=True)
        ttk.Label(table, text="Gesture", font=("TkDefaultFont", 10, "bold")).grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 6)
        )
        ttk.Label(table, text="Function", font=("TkDefaultFont", 10, "bold")).grid(
            row=0, column=1, sticky="w"
        )

        for r, g in enumerate(self.gestures, start=1):
            ttk.Label(table, text=g).grid(row=r, column=0, sticky="w", padx=(0, 8), pady=4)

            sv = tk.StringVar(value=self.defaults.get(g, ""))
            self.vars[g] = sv

            row_frame = ttk.Frame(table)
            row_frame.grid(row=r, column=1, sticky="ew", pady=4)
            table.grid_columnconfigure(1, weight=1)
            row_frame.grid_columnconfigure(0, weight=1)

            combo = ttk.Combobox(row_frame, values=[""] + self.choices,
                                 state="readonly", textvariable=sv)
            combo.grid(row=0, column=0, sticky="ew")
            combo.set(self.defaults.get(g, ""))

        # Buttons
        btns = ttk.Frame(container)
        btns.pack(fill="x", pady=(10, 0))

        ttk.Button(btns, text="Save to config file", command=self.save_config).pack(side="left")
        ttk.Button(btns, text="Reset", command=self.reset_to_defaults).pack(side="left", padx=6)
        ttk.Button(btns, text="Close", command=self.finish_and_close).pack(side="right")


    def _load_mappings(self, path: Path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert isinstance(data, list)
            for entry in data:
                assert all(k in entry for k in ("gesture", "function", "hexkey"))
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read {path}:\n{e}")
            self.destroy()
            sys.exit(1)

    def get_mapping(self) -> dict[str, str]:
        """Return gesture -> selected function name."""
        return {g: self.vars[g].get().strip() for g in self.gestures}

    def get_resolved_mapping(self) -> dict[str, list[str]]:
        """Return gesture -> hex key(s) from common_actions."""
        mapping = self.get_mapping()
        return {g: self.common_actions.get(func, []) for g, func in mapping.items()}

    def reset_to_defaults(self):
        for g in self.gestures:
            self.vars[g].set(self.defaults.get(g, ""))

    def save_config(self):
        """Save to user_mappings.json"""
        user_path = self.mappings_path.parent / "user_mappings.json"
        result = []
        mapping = self.get_mapping()
        for g in self.gestures:
            func = mapping[g]
            hexkey = self.common_actions.get(func, [])
            result.append({"gesture": g, "function": func, "hexkey": hexkey})
        with open(user_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        messagebox.showinfo("Saved", f"Saved to {user_path}")

    def finish_and_close(self):
        print("Current mappings (functions):", self.get_mapping())
        print("Resolved mappings (hex):", self.get_resolved_mapping())
        self.destroy()


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    default_path = base_dir / "settings" / "default_mappings.json"
    user_path = base_dir / "settings" / "user_mappings.json"

    chosen_path = user_path if user_path.exists() else default_path

    if not default_path.exists():
        sys.exit("Error: default_mappings.json not found.")

    app = GesturePanel(chosen_path)
    app.mainloop()
