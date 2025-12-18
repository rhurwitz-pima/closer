import argparse
import csv
import sys
from itertools import batched
from pathlib import Path


def make_parser():
    parser = argparse.ArgumentParser(
        prog="closer",
        description="Converts a D2L grade CSV to an eLumen CLO CSV",
        epilog="For additional information contact Roger Hurwitz",
    )
    parser.add_argument(
        "input_fname",
        help="The path to the source D2L CSV to read.",
    )
    parser.add_argument(
        "output_fname",
        help="The destination path where the CLO CSV will be written.",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=70,
        help="Integer percent at or above which CLOs will meet expectations.",
    )

    return parser


def make_scores(line: list[str]) -> list[float]:
    scores = [
        float(numerator) / float(denominator)
        for numerator, denominator in batched(line, n=2)
    ]
    return scores


def make_meets(scores: list[float], threshold: float) -> list[str]:
    meets = ["1" if score >= threshold else "0" for score in scores]
    return meets


def main(input_fname: str, output_fname: str, threshold: float):
    input_path, output_path = Path(input_fname), Path(output_fname)
    output_rows: list[list[str]] = []
    clo_count = 0

    with input_path.open(encoding="utf-8", newline="") as f:
        csv_reader = csv.reader(f)
        input_header = next(csv_reader)
        clo_count = (len(input_header) - 2) // 2
        for input_line in csv_reader:
            student_id = input_line[0][1:]  # strip leading hash from student ID
            scores = make_scores(input_line[1:-1])  # exclude trailing hash in line
            meets = make_meets(scores, threshold)
            output_row = [student_id] + meets
            output_rows.append(output_row)

    if not output_rows:
        sys.exit(1)

    output_header = ["SID"] + ["CLO_" + str(clo_id) for clo_id in range(1, clo_count + 1)]

    with output_path.open(mode="w", encoding="utf-8", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(output_header)
        csv_writer.writerows(output_rows)


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()
    print(args.threshold)
    main(args.input_fname, args.output_fname, args.threshold / 100)
