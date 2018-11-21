"""
A generic wrapper script for the pyfreeipa Api class
"""
import json
import sys
from pyfreeipa.api import Api
from pyfreeipa.configuration import CONFIG


def main():
    """
    @brief      This provides a wrapper for the pyfreeipa module

    @return     { description_of_the_return_value }
    """

    if CONFIG['command'] == 'dumpconfig':
        print(json.dumps(CONFIG, indent=4, sort_keys=True))
        sys.exit(0)

    # Define API session
    ipaapi = Api(
        host=CONFIG['ipaserver']['host'],
        username=CONFIG['ipaserver']['user'],
        password=CONFIG['ipaserver']['password'],
        port=CONFIG['ipaserver']['port'],
        verify_ssl=CONFIG['ipaserver']['verify_ssl'],
        verify_method=CONFIG['ipaserver']['verify_method'],
        verify_warnings=CONFIG['ipaserver']['verify_warnings'],
        dryrun=CONFIG['dryrun']
    )

    if CONFIG['uid']:
        response = ipaapi.otptoken_show(
            CONFIG['uid']
        )
    else:
        print("Requires a otptoken uniqueid specified with --uid")
        sys.exit(1)

    print(json.dumps(response.json(), indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
