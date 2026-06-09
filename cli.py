import argparse
import json
import os
import sys

import requests


DEFAULT_API_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000/analyze"
)


def analyze(input_file, output_file, api_url):

    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        sys.exit(1)

    try:

        with open(input_file, "r") as f:
            payload = json.load(f)

    except json.JSONDecodeError:
        print("Invalid JSON input file")
        sys.exit(1)

    try:

        response = requests.post(
            api_url,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

    except requests.exceptions.Timeout:
        print("Request timed out")
        sys.exit(3)

    except requests.exceptions.ConnectionError:
        print("Unable to connect to API")
        sys.exit(2)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(2)

    try:

        with open(output_file, "w") as f:
            json.dump(
                result,
                f,
                indent=4
            )

    except Exception as e:
        print(f"Unable to write output file: {e}")
        sys.exit(1)

    print("\nAnalysis Complete")
    print(f"Input  : {input_file}")
    print(f"Output : {output_file}")
    print(f"Decision : {result.get('decision')}")
    print(f"Risk Score : {result.get('risk_score')}")

    sys.exit(0)


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(
    dest="command"
)

analyze_parser = subparsers.add_parser(
    "analyze"
)

analyze_parser.add_argument(
    "--input",
    required=True,
    help="Path to input JSON file"
)

analyze_parser.add_argument(
    "--output",
    required=True,
    help="Path to output JSON file"
)

analyze_parser.add_argument(
    "--api-url",
    default=DEFAULT_API_URL,
    help="Analyze endpoint URL"
)

args = parser.parse_args()

if args.command == "analyze":

    analyze(
        args.input,
        args.output,
        args.api_url
    )

else:
    parser.print_help()
    sys.exit(1)