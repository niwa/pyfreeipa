"""
{ item_description }
"""
import json
import pyfreeipa.configuration

CONFIG = pyfreeipa.configuration.Configuration()


def main():
    print(json.dumps(CONFIG, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
