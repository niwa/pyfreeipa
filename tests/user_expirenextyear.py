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

    users = []

    if CONFIG['users'] and CONFIG['groups']:
        if isinstance(CONFIG['groups'], list):
            for group in CONFIG['groups']:
                someusers = ipaapi.users(
                    uid=CONFIG['users'],
                    in_group=group
                )
                users = users + someusers
        else:
            users = ipaapi.users(
                uid=CONFIG['users'],
                in_group=CONFIG['groups']
            )
    elif CONFIG['users']:
        users = ipaapi.users(CONFIG['users'])
    elif CONFIG['groups']:
        if isinstance(CONFIG['groups'], list):
            for group in CONFIG['groups']:
                someusers = ipaapi.users(
                    uid=CONFIG['users'],
                    in_group=group
                )
                users = users + someusers
        else:
            users = ipaapi.users(in_group=CONFIG['groups'])
    else:
        users = ipaapi.users()

    users = list({v['uid']: v for v in users}.values())

    today = datetime.date.today()
    themonth = today.month + 1
    theyear = today.year + 1
    if themonth > 12:
        themonth = themonth - 12
        theyear = theyear + 1
    nextmonth = today.replace(
        year=theyear,
        month=themonth,
        day=1
    )
    expiringusers = {}
    havepassword = 0
    nopassword = 0

    for user in users:
        if 'krbpasswordexpiration' in user:
            havepassword += 1
            expiry = user['krbpasswordexpiration']
            if isinstance(expiry, datetime.datetime):
                if today <= expiry.date() <= nextmonth:
                    theday = expiry.day
                    if theday > 28:
                        theday = 28
                    themonth = expiry.month + 1
                    theyear = expiry.year + 1
                    if themonth > 12:
                        themonth = themonth - 12
                        theyear = theyear + 1
                    newexpiry = expiry.replace(
                        year=theyear,
                        month=themonth,
                        day=theday
                    )
                    expiringusers[user['uid']] = {
                        'expiry': expiry,
                        'newexpiry': newexpiry
                    }
        else:
            nopassword += 1

    print("Gathered %s users" % len(users))
    print("Users with password: %s" % havepassword)
    print("Users without password: %s" % nopassword)
    print("Total expiring users: %s\n" % len(expiringusers))

    if CONFIG['dryrun']:
        print(
            "Users with passwords expiring between %s and %s:\n%s" %
            (
                str(today),
                str(nextmonth),
                json.dumps(
                    expiringusers,
                    indent=2,
                    sort_keys=True,
                    default=str
                )
            )
        )

    responses = []

    for user in expiringusers:
        response = ipaapi.user_mod(
            user,
            krbpasswordexpiration=expiringusers[user]['newexpiry']
        )

        responses.append(response)

    if CONFIG['dryrun']:
        for modresponse in responses:
            prettyprintpost(modresponse)
    else:
        for modresponse in responses:
            print(
                json.dumps(
                    modresponse.json(),
                    indent=2,
                    sort_keys=True,
                    default=str
                )
            )


def prettyprintpost(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    Brutally copypasted from: https://stackoverflow.com/a/23816211
    """
    jsonbody = json.loads(req.body)
    body = json.dumps(jsonbody, indent=2, sort_keys=True)
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        body
    ))

if __name__ == "__main__":
    main()
