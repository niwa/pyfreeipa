"""
Methods for users
"""
from typing import Union
import pyfreeipa.util

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

    response = self.user_show(uid, allattrs=True)

    if response.json()['result']:
        return response.json()['result']['result']
    else:
        return None


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

    if response.json()['result']:
        return response.json()['result']['result']
    else:
        return []


def user_list(
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
                        userlist.append(user['uid'][0])
            else:
                response = self.users(uid=uids)
                for user in response:
                    userlist.append(user['uid'][0])
        if groups:
            if isinstance(groups, list):
                for groupname in groups:
                    response = self.users(in_group=groupname)
                    for user in response:
                        userlist.append(user['uid'][0])
            else:
                response = self.users(in_group=groups)
                for user in response:
                    userlist.append(user['uid'][0])
    else:
        for user in self.users():
            userlist.append(user['uid'][0])

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
