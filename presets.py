import os
import json

PRESET_FOLDER = "configs/rule_presets"

def list_presets():
    return os.listdir(PRESET_FOLDER)

def load_preset(name):
    path = os.path.join(PRESET_FOLDER, name)
    with open(path) as f:
        return json.load(f)