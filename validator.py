def validate_rules(required, actual):
    results = []

    for rule, req_value in required.items():
        act_value = actual.get(rule)

        if act_value is None:
            status = "MISSING"
            act_value = "N/A"
        else:
            status = "PASS" if act_value >= req_value else "FAIL"

        results.append({
            "rule": rule,
            "required": req_value,
            "actual": act_value,
            "status": status
        })

    return results