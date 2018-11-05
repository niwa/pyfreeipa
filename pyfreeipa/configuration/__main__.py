"""
Process command line arguments and/or load configuration file
"""
import json
import yaml
import argparse


def configuration():
    args = _do_args()
    print(json.dumps(args, indent=4, sort_keys=True))


def _do_args():
    # Parse command line arguments and modify config
    parser = argparse.ArgumentParser(description='Python FreeIPA tools')

    # Command line arguments, the help value describes each argument's purpose
    parser.add_argument(
        "-v",
        "--verbose",
        dest='verbose',
        help="Increase output to stderr and stdout",
        action="store_true"
    )

    parser.add_argument(
        "-q",
        "--quiet",
        dest='quiet',
        help="Reduce output to stderr and stdout",
        action="store_true"
    )

    parser.add_argument(
        "-d",
        "--dry_run",
        dest='dry_run',
        help="Do a dry run, no changes written to IPA server",
        action="store_true"
    )

    parser.add_argument(
        "-f",
        "--file",
        default=None,
        dest='file',
        help="Specify a configuration file",
    )

    return parser.parse_args()

if __name__ == "__main__":
    configuration()
