import xml.etree.ElementTree as ET

def parse_altium_rules(file_path):
    rules = {}

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Generic rule parsing
        for rule in root.iter():
            name = rule.get("Name")
            value = rule.get("Value")

            if name and value:
                try:
                    rules[name] = float(value)
                except ValueError:
                    continue

    except Exception as e:
        print(f"XML Parse Error: {e}")

    return rules