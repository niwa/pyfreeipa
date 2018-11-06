"""
{ item_description }
"""
import json
import sys
import pyfreeipa.configuration
from pyfreeipa.api import Api

CONFIG = pyfreeipa.configuration.Configuration()


def main():

    if CONFIG.command == 'dumpconfig':
        print(json.dumps(vars(CONFIG), indent=4, sort_keys=True))
        sys.exit(0)

    # Define API session
    ipaapi = Api(
        host=CONFIG.ipaserver['host'],
        username=CONFIG.ipaserver['user'],
        password=CONFIG.ipaserver['password'],
        port=CONFIG.ipaserver['port'],
        verify_ssl=CONFIG.ipaserver['verify_ssl'],
        verify_method=CONFIG.ipaserver['verify_method'],
        verify_warnings=CONFIG.ipaserver['verify_warnings'],
        dryrun=CONFIG.dryrun
    )

    if CONFIG.command == 'connectiontest':
        print(
            "Test connection to %s" %
            CONFIG.ipaserver['host']
        )
        response = ipaapi.login()
        if response.status_code != 200:
            print(
                'Failed to log %s in to %s' %
                (
                    CONFIG.ipaserver['user'],
                    CONFIG.ipaserver['host']
                )
            )
        else:
            print(
                'Successfully logged in as %s on %s' %
                (
                    CONFIG.ipaserver['user'],
                    CONFIG.ipaserver['host']
                )
            )

    else:
        print("Does nothing")


if __name__ == "__main__":
    main()
