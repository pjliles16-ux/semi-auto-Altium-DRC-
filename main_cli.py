import json
import sys
from core.parser import parse_altium_rules
from core.comparator import compare_rules
from core.report_generator import generate_report
from core.logger import setup_logger, log_info

def main():

    if len(sys.argv) != 3:
        print("Usage: python main_cli.py <board.xml> <preset.json>")
        return

    setup_logger()

    board_file = sys.argv[1]
    preset_file = sys.argv[2]

    with open(preset_file) as f:
        required = json.load(f)

    actual = parse_altium_rules(board_file)

    results, summary = compare_rules(required, actual)

    txt, csv = generate_report(results, summary)

    log_info("Validation completed.")
    print("Validation complete.")
    print(f"Reports saved:\n{txt}\n{csv}")

if __name__ == "__main__":
    main()