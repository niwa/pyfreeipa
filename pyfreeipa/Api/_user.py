"""
Methods for users
"""
from datetime import datetime
from typing import Union
from ._utils import delist, listdelist

def user(
        self,
        uid: str
):
    """
    @brief      Returns only the user response

    @param      self  The object
    @param      uid   The uid of the user to return

    @return     the user account as a dictionary
    """

    user = None
    response = self.user_show(uid, allattrs=True)

    if response.json()['result']:
        user = delist(response.json()['result']['result'])

    return user


def users(
        self,
        searchstring: Union[str, None]=None,
        uid: Union[str, None]=None,
        uidnumber: Union[int, None]=None,
        in_group: Union[str, list, None]=None,
        mail: Union[str, list, None]=None,
):
    """
    @brief      Given a some search parameters find all the user acounts that match

    @param      self          The object
    @param      searchstring  The searchstring used on any otptoken attribute
    @param      uniqueid      substring used to match otptoken uniqueid
    @param      owner         search for tokens owned but specified user

    @return     { description_of_the_return_value }
    """

    response = self.user_find(
        searchstring=searchstring,
        uid=uid,
        uidnumber=uidnumber,
        in_group=in_group,
        mail=mail,
        allattrs=True
    )

    userlist = []

    if response.json()['result']:
        userlist = listdelist(response.json()['result']['result'])

    return userlist


def userlist(
        self,
        uids: Union[str, list, None]=None,
        groups: Union[str, list, None]=None
):
    """
    @brief      Given a list of uids and/or groups, return a list of usernames that match or are members

    @param      self          The object
    @param      searchstring  The searchstring used on any otptoken attribute
    @param      uniqueid      substring used to match otptoken uniqueid
    @param      owner         search for tokens owned but specified user

    @return     { description_of_the_return_value }
    """

    userlist = []

    if uids or groups:
        if uids:
            if isinstance(uids, list):
                for username in uids:
                    response = self.users(uid=username)
                    for user in response:
                        userlist.append(user['uid'])
            else:
                response = self.users(uid=uids)
                for user in response:
                    userlist.append(user['uid'])
        if groups:
            if isinstance(groups, list):
                for groupname in groups:
                    response = self.users(in_group=groupname)
                    for user in response:
                        userlist.append(user['uid'])
            else:
                response = self.users(in_group=groups)
                for user in response:
                    userlist.append(user['uid'])
    else:
        for user in self.users():
            userlist.append(user['uid'])

    return sorted(set(userlist))

def user_show(
        self,
        uid: str,
        rights: Union[bool, None]=None,
        allattrs: Union[bool, None]=None,
        raw: Union[bool, None]=None
):
    """
    @brief      A complete implementation of the user_show command

    @param      self  The object

    @param      uid of the user to be shown

    @param      rights, if true, displays the access rights of this user

    @param      all, retrieves all attributes

    @param      raw, returns the raw response, only changes output format

    @return     the requests.Response from the ping request
    """

    method = 'user_show'

    args = uid

    params = {}

    if rights is not None:
        params['rights'] = rights

    if allattrs is not None:
        params['all'] = allattrs

    if raw is not None:
        params['raw'] = raw

    return self.request(
        method,
        args=args,
        params=params
    )


def user_find(
        self,
        searchstring: Union[str, None]=None,
        uid: Union[str, None]=None,
        uidnumber: Union[int, None]=None,
        in_group: Union[str, list, None]=None,
        mail: Union[str, list, None]=None,
        rights: Union[bool, None]=None,
        allattrs: Union[bool, None]=None,
        raw: Union[bool, None]=None
):
    """
    @brief      A partial implementation of the user_find request

    @param      self  The object

    @param      uid of the user to be shown

    @param      rights, if true, displays the access rights of this user

    @param      all, retrieves all attributes

    @param      raw, returns the raw response, only changes output format

    @return     the requests.Response from the ping request
    """

    method = 'user_find'

    args = None

    if searchstring:
        args = searchstring

    params = {}

    if uid is not None:
        params['uid'] = uid

    if uidnumber is not None:
        params['uidnumber'] = uidnumber

    if in_group is not None:
        params['in_group'] = in_group

    if mail is not None:
        params['mail'] = mail

    if rights is not None:
        params['rights'] = rights

    if allattrs is not None:
        params['all'] = allattrs

    if raw is not None:
        params['raw'] = raw

    return self.request(
        method,
        args=args,
        params=params
    )


def user_getattr(
        self,
        uid: type=str,
        attribute: type=str
):
    user = self.user(uid=uid)

    attributevalue = None

    if attribute in user:
        attributevalue = user[attribute]

    return attributevalue


# Write methods that may cause changes to the directory
# These methods MUST require dryrun to be false to write changes
def user_mod(
        self,
        # Arguments
        uid: type=str,
        # Options
        givenname: Union[str, None]=None,
        sn: Union[str, None]=None,
        cn: Union[str, None]=None,
        displayname: Union[str, None]=None,
        initials: Union[str, None]=None,
        homedirectory: Union[str, None]=None,
        gecos: Union[str, None]=None,
        loginshell: Union[str, None]=None,
        krbprincipalname: Union[str, None]=None,
        krbprincipalexpiration: Union[datetime, None]=None,
        krbpasswordexpiration: Union[datetime, None]=None,
        mail: Union[str, None]=None,
        userpassword: Union[str, None]=None,
        random: Union[bool, None]=None,
        uidnumber: Union[int, None]=None,
        gidnumber: Union[int, None]=None,
        telephonenumber: Union[str, None]=None,
        mobile: Union[str, None]=None,
        ou: Union[str, None]=None,
        title: Union[str, None]=None,
        manager: Union[str, None]=None,
        carlicense: Union[str, None]=None,
        ipasshpubkey: Union[str, None]=None,
        ipauserauthtype: Union[str, None]=None,
        userclass: Union[str, None]=None,
        ipatokenradiusconfiglink: Union[str, None]=None,
        ipatokenradiususername: Union[str, None]=None,
        departmentnumber: Union[str, None]=None,
        employeenumber: Union[str, None]=None,
        employeetype: Union[str, None]=None,
        preferredlanguage: Union[str, None]=None,
        nsaccountlock: Union[str, None]=None,
        no_members: Union[bool, None]=None,
        rename: Union[str, None]=None,
        allattrs: Union[bool, None]=None,
        raw: Union[bool, None]=None
):

    method = 'user_mod'

    args = uid

    params = {}

    if givenname is not None:
        params['givenname'] = givenname

    if sn is not None:
        params['sn'] = sn

    if cn is not None:
        params['cn'] = cn

    if displayname is not None:
        params['displayname'] = displayname

    if initials is not None:
        params['initials'] = initials

    if homedirectory is not None:
        params['homedirectory'] = homedirectory

    if gecos is not None:
        params['gecos'] = gecos

    if loginshell is not None:
        params['loginshell'] = loginshell

    if krbprincipalname is not None:
        params['krbprincipalname'] = krbprincipalname

    if krbprincipalexpiration is not None:
        params['krbprincipalexpiration'] = krbprincipalexpiration.strftime("%Y%m%d%H%M%SZ")

    if krbpasswordexpiration is not None:
        params['krbpasswordexpiration'] = krbpasswordexpiration.strftime("%Y%m%d%H%M%SZ")

    if mail is not None:
        params['mail'] = mail

    if userpassword is not None:
        params['userpassword'] = userpassword

    if random is not None:
        params['random'] = random

    if uidnumber is not None:
        params['uidnumber'] = uidnumber

    if gidnumber is not None:
        params['gidnumber'] = gidnumber

    if telephonenumber is not None:
        params['telephonenumber'] = telephonenumber

    if mobile is not None:
        params['mobile'] = mobile

    if ou is not None:
        params['ou'] = ou

    if title is not None:
        params['title'] = title

    if manager is not None:
        params['manager'] = manager

    if carlicense is not None:
        params['carlicense'] = carlicense

    if ipasshpubkey is not None:
        params['ipasshpubkey'] = ipasshpubkey

    if ipauserauthtype is not None:
        params['ipauserauthtype'] = ipauserauthtype

    if userclass is not None:
        params['userclass'] = userclass

    if ipatokenradiusconfiglink is not None:
        params['ipatokenradiusconfiglink'] = ipatokenradiusconfiglink

    if ipatokenradiususername is not None:
        params['ipatokenradiususername'] = ipatokenradiususername

    if departmentnumber is not None:
        params['departmentnumber'] = departmentnumber

    if employeenumber is not None:
        params['employeenumber'] = employeenumber

    if employeetype is not None:
        params['employeetype'] = employeetype

    if preferredlanguage is not None:
        params['preferredlanguage'] = preferredlanguage

    if nsaccountlock is not None:
        params['nsaccountlock'] = nsaccountlock

    if no_members is not None:
        params['no_members'] = no_members

    if rename is not None:
        params['rename'] = rename

    if allattrs is not None:
        params['all'] = allattrs

    if raw is not None:
        params['raw'] = raw

    prepared = self.preprequest(
        method,
        args=args,
        params=params
    )

    if not self._dryrun:
        response = self._session.send(prepared)
    else:
        response = prepared

    return response
