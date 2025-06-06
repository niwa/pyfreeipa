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
        print(json.dumps(CONFIG, indent=2, sort_keys=True))
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
        response = ipaapi.user_find(
            uid=CONFIG['users'],
            in_group=CONFIG['groups']
        )
        users = ipaapi.users(
            uid=CONFIG['users'],
            in_group=CONFIG['groups']
        )
    elif CONFIG['users']:
        response = ipaapi.user_find(
            CONFIG['users']
        )
        users = ipaapi.users(CONFIG['users'])
    elif CONFIG['groups']:
        response = ipaapi.user_find(
            in_group=CONFIG['groups']
        )
        users = ipaapi.users(in_group=CONFIG['groups'])
    else:
        response = ipaapi.user_find()
        users = ipaapi.users()
    deltatime = datetime.now() - starttime

    print("The request")
    print(response.request.body)

    print("Raw response:")
    print(json.dumps(response.json(), indent=2, sort_keys=True))

    print("Response as a list object:")
    print(json.dumps(users, indent=2, sort_keys=True, default=str))

    print("Elapsed time for query: %s" % deltatime)


if __name__ == "__main__":
    main()
