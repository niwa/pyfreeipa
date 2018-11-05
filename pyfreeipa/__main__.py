"""
{ item_description }
"""
import json
import sys
import pyfreeipa.configuration

CONFIG = pyfreeipa.configuration.Configuration()


def main():

    if CONFIG.command == 'dumpconfig':
        print(json.dumps(vars(CONFIG), indent=4, sort_keys=True))
        sys.exit(0)

    if CONFIG.command == 'connectiontest':
        print(
            "Test connection to %s" %
            CONFIG.ipaserver['host']
        )

    else:
        print("Does nothing")


if __name__ == "__main__":
    main()
