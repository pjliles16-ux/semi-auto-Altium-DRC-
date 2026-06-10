def compare_rules(required, actual, tolerance_percent=0):

    results = []
    summary = {"CRITICAL": 0, "WARNING": 0, "INFO": 0}

    for rule_name, required_data in required.items():

        required_value = required_data["value"]
        severity = required_data["severity"]

        actual_value = actual.get(rule_name)

        if actual_value is None:
            status = "FAIL"
            message = "Rule missing"
        else:
            allowed = required_value * (tolerance_percent / 100)

            if actual_value >= required_value - allowed:
                status = "PASS"
                message = "Within limits"
            else:
                status = "FAIL"
                message = f"{actual_value} < {required_value}"

        if status == "FAIL":
            summary[severity] += 1

        results.append({
            "rule": rule_name,
            "status": status,
            "severity": severity,
            "message": message
        })

    return results, summary