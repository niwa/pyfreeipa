"""
{ item_description }
"""
import json
import pyfreeipa.configuration

CONFIG = pyfreeipa.configuration.Configuration()


def main():
    if CONFIG.command == 'dumpconfig':
        print(json.dumps(vars(CONFIG), indent=4, sort_keys=True))
    else:
        print("Does nothing")


if __name__ == "__main__":
    main()
