import argparse
import csv
import re
import sys
from itertools import batched
from pathlib import Path
from typing import Iterator

# Regex pattern to validate and capture D2L CSV input rows
D2L_PATTERN = re.compile(
    r"""
    ^                       # Start of the line
    \#                      # Literal D2L start marker (hash)
    (A0\d{7})               # GROUP 1: Student ID (e.g. A01234567)
    ,                       # Separator after ID
    (                       # GROUP 2: The Score Data (Start)
      (?:                   # Non-capturing group for repeated pairs:
        [0-9.]+             #   Numerator
        ,                   #   Separator
        [0-9.]+             #   Denominator
        ,                   #   Trailing comma
      )*                    # Repeat 0 or more times
      [0-9.]+               # Final Pair Numerator
      ,                     # Separator
      [0-9.]+               # Final Pair Denominator
    )                       # GROUP 2: End
    ,\#                     # Literal trailing comma and hash
    $                       # End of the line
""",
    re.VERBOSE,
)


def make_parser():
    """Construct the argparse parser for command line inputs."""
    parser = argparse.ArgumentParser(
        prog="closer",
        description="Converts D2L CSV to eLumen with strict validation.",
    )
    parser.add_argument("input_fname", help="Path to source D2L CSV.")
    parser.add_argument("output_fname", help="Path to destination CSV.")
    parser.add_argument(
        "-t", "--threshold", type=int, default=70, help="Passing percent (e.g. 70)."
    )
    return parser


def yield_student_data(path: Path) -> Iterator[tuple[str, str]]:
    """Yields valid student data or exits if a malformed student row is found."""
    with path.open(encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            if not (line := line.strip()):  # strip line and skip if empty
                continue

            match = D2L_PATTERN.match(line)

            if match:  # no issues, fully matches valid pattern
                yield match.group(1), match.group(2)

            elif line.startswith("#"):  # data D2L row, but malformed
                print(f"❌ Error: Malformed data found on line {line_num}.")
                print(f"Content: {line}")
                print("Expected format: #StudentId,Num,Denom,Num,Denom,...,#")
                sys.exit(1)

            else:  # non-data D2L row (e.g., header), safe to skip
                pass


def process_scores(scores_str: str, threshold: float) -> list[str]:
    """Splits the clean numeric string "10,20,30,40" into pairs and grades them."""
    raw_values = scores_str.split(",")
    results: list[str] = []

    for num_str, den_str in batched(raw_values, 2):
        numerator = float(num_str)
        denominator = float(den_str)

        try:
            score = numerator / denominator
            results.append("1" if score >= threshold else "0")
        except ZeroDivisionError:
            print(f"❌ Error: Invalid scores string in D2L file: {scores_str}")
            sys.exit(1)

    return results


def main():
    parser = make_parser()
    args = parser.parse_args()

    input_path = Path(args.input_fname)
    output_path = Path(args.output_fname)
    threshold_decimal = args.threshold / 100.0

    if not input_path.exists():
        print(f"❌ Error: Input file '{input_path}' not found.")
        sys.exit(1)

    output_rows: list[list[str]] = []

    # 1. READ & PROCESS
    for student_id, scores_str in yield_student_data(input_path):
        meets_expectations = process_scores(scores_str, threshold_decimal)
        output_rows.append([student_id] + meets_expectations)

    if not output_rows:
        print("❌ Error: No valid student records found.")
        sys.exit(1)

    # 2. WRITE OUTPUT
    clo_count = len(output_rows[0]) - 1
    headers = ["SID"] + [f"CLO_{i + 1}" for i in range(clo_count)]

    with output_path.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(output_rows)

    print(f"✅ Successfully converted {len(output_rows)} records to {output_path}")


if __name__ == "__main__":
    main()
