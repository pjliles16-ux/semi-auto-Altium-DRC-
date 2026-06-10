def compare_with_tolerance(required, actual, tolerance_percent=10):
    results = []

    for rule, req_value in required.items():
        act_value = actual.get(rule)

        if act_value is None:
            status = "MISSING"
            act_value = "N/A"
        else:
            lower_bound = req_value * (1 - tolerance_percent / 100)
            status = "PASS" if act_value >= lower_bound else "FAIL"

        results.append({
            "rule": rule,
            "required": f"{req_value} ±{tolerance_percent}%",
            "actual": act_value,
            "status": status
        })

    return results