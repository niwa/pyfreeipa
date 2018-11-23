"""
A generic wrapper script for the pyfreeipa Api class
"""
import json
import sys
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

    tokens = ipaapi.otptokens(CONFIG['uid'])

    for token in tokens:
        token_managers = list(CONFIG['otptoken']['managedby'])
        if 'ipatokenowner' in token:
            if CONFIG['otptoken']['ownermanagedby']:
                token_managers.append(token['ipatokenowner'][0])

        if 'managedby_user' in token:
            current_managers = token['managedby_user']
            if set(current_managers) == set(token_managers):
                state = 'Matches'
            else:
                state = 'No match'
        else:
            current_managers = []
            state = "No managers"

        print(
            "%s: %s current:%s expected:%s" %
            (
                state,
                token['ipatokenuniqueid'][0],
                current_managers,
                token_managers
            )
        )


if __name__ == "__main__":
    main()
