import json
import os
from datetime import datetime

def save_session(tree):
    data = []

    for row in tree.get_children():
        data.append(tree.item(row)["values"])

    if not os.path.exists("sessions"):
        os.makedirs("sessions")

    filename = f"sessions/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    return filename