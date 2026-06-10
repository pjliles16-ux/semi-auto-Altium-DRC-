import json
import os

PRESET_FOLDER = "configs/rule_presets"

MANUFACTURER_MAP = {
    "JLCPCB": "jlcpcb.json",
    "PCBWay": "pcbway.json",
    "InHouse": "inhouse.json"
}

def load_manufacturer_rules(name):
    if name not in MANUFACTURER_MAP:
        raise ValueError("Unknown manufacturer")

    path = os.path.join(PRESET_FOLDER, MANUFACTURER_MAP[name])

    with open(path) as f:
        return json.load(f)