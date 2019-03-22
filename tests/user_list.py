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
    if CONFIG['users'] and CONFIG['groups']:
        users = ipaapi.user_list(
            uids=CONFIG['users'],
            groups=CONFIG['groups']
        )
    elif CONFIG['users']:
        users = ipaapi.user_list(uids=CONFIG['users'])
    elif CONFIG['groups']:
        users = ipaapi.user_list(groups=CONFIG['groups'])
    else:
        users = ipaapi.user_list()

    deltatime = datetime.now() - starttime

    print("Response as a list object:")
    print(json.dumps(users, indent=4, sort_keys=True))
    print("Number of users: %s" % len(users))
    print("Elapsed time for query: %s" % deltatime)

if __name__ == "__main__":
    main()
