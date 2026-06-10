import csv
import os
from datetime import datetime

def generate_report(results, summary):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    txt_file = f"reports/DRC_Report_{timestamp}.txt"
    csv_file = f"reports/DRC_Report_{timestamp}.csv"

    # TXT Report
    with open(txt_file, "w") as f:
        f.write("PCB RULE VALIDATION REPORT\n\n")
        for r in results:
            f.write(f"{r['rule']} | {r['status']} | {r['severity']} | {r['message']}\n")

        f.write("\nSUMMARY\n")
        for k, v in summary.items():
            f.write(f"{k}: {v}\n")

    # CSV Report
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Rule", "Status", "Severity", "Message"])
        for r in results:
            writer.writerow([r["rule"], r["status"], r["severity"], r["message"]])

    return txt_file, csv_file