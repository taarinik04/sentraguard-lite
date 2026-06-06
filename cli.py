import argparse
import json
import requests

API_URL = "http://127.0.0.1:8000/analyze"


def analyze(input_file, output_file):

    with open(input_file, "r") as f:
        payload = json.load(f)

    response = requests.post(
        API_URL,
        json=payload
    )

    result = response.json()

    with open(output_file, "w") as f:
        json.dump(
            result,
            f,
            indent=4
        )

    print("\n✅ Analysis Complete")
    print(f"Input  : {input_file}")
    print(f"Output : {output_file}")


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest="command")

analyze_parser = subparsers.add_parser("analyze")

analyze_parser.add_argument(
    "--input",
    required=True
)

analyze_parser.add_argument(
    "--output",
    required=True
)

args = parser.parse_args()

if args.command == "analyze":

    analyze(
        args.input,
        args.output
    )