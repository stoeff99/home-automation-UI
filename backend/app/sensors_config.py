import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "sensors.json")

def load_sensors_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
