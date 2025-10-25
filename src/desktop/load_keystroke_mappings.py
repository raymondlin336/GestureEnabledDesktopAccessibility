import json

def load_keystrokes(json_path="Settings/default_mappings.json"):

    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: 'data.json' not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in 'data.json'.")
