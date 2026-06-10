class Rule:
    def __init__(self, name, value, severity="CRITICAL"):
        self.name = name
        self.value = value
        self.severity = severity

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "severity": self.severity
        }