MM_TO_MIL = 39.3701

def convert(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value

    if from_unit == "mm" and to_unit == "mil":
        return value * MM_TO_MIL

    if from_unit == "mil" and to_unit == "mm":
        return value / MM_TO_MIL

    raise ValueError("Unsupported unit conversion")