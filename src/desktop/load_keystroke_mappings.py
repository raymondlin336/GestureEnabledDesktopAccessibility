import json

def load_keystrokes():
    default_path = "Settings/default_mappings.json"
    user_path = "Settings/user_mappings.json"
    try:
        with open(user_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        try:
            with open(default_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print("Neither JSON files were found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in 'data.json'.")
