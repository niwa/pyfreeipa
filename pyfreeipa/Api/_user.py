"""
Methods for users
"""
from typing import Union


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
