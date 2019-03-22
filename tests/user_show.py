"""
A generic wrapper script for the pyfreeipa Api class
"""
import json
import sys
from datetime import datetime
from pyfreeipa.Api import Api
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

    starttime = datetime.now()
    if CONFIG['users']:
        if len(CONFIG['users']) == 1:
            response = ipaapi.user_show(
                CONFIG['users'][0]
            )
            user = ipaapi.user(
                CONFIG['users'][0]
            )
        else:
            sys.exit("Requires a single uid/username specified with --uid")
    else:
        sys.exit("Requires an account uid/username specified with --uid")
    deltatime = datetime.now() - starttime

    print("The request:")
    print(response.request.body)

    print("Raw response:")
    print(json.dumps(response.json(), indent=4, sort_keys=True))

    print("Response as a dict:")
    print(json.dumps(user, indent=4, sort_keys=True))
    print("Elapsed time for query: %s" % deltatime)

if __name__ == "__main__":
    main()
