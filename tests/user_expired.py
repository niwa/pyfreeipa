"""
A generic wrapper script for the pyfreeipa Api class
"""
import json
import sys
import datetime
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

    if CONFIG['users'] and CONFIG['groups']:
        users = ipaapi.users(
            uid=CONFIG['users'],
            in_group=CONFIG['groups']
        )
    elif CONFIG['users']:
        users = ipaapi.users(CONFIG['users'])
    elif CONFIG['groups']:
        users = ipaapi.users(in_group=CONFIG['groups'])
    else:
        users = ipaapi.users()

    today = datetime.date.today()
    margin = datetime.timedelta(days=7)
    month = datetime.timedelta(days=30)
    inaweek = today + margin
    lastmonth = today - month
    expiringusers = []

    for user in users:
        if 'krbpasswordexpiration' in user:
            expiry = user['krbpasswordexpiration']
            if isinstance(expiry, datetime.datetime):
                if lastmonth <= expiry.date() <= inaweek:
                    userhash = {
                        'name': user['displayname'],
                        'uid': user['uid'],
                        'email': user['mail'],
                        'passwdexpiry': expiry
                    }
                    expiringusers.append(userhash)

    print("Users with passwords expired in the last 30 days, and in the next week:")
    print(json.dumps(expiringusers, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
