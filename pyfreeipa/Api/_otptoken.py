"""
Methods for otptokens
otp - one time password, used for two factor & multifactor authentication.
"""
from typing import Union


def otptoken_find(
        self,
        searchstring: Union[str, None]=None,
        uniqueid: Union[str, None]=None,
        owner: Union[str, None]=None,
        no_members: Union[bool, None]=None,
        allattrs: Union[bool, None]=None,
        raw: Union[bool, None]=None
):
    """
    @brief Partial implementation the otptoken_show request, only searches by parameters below

    @param self The object
    @param uniqueid, the unique identifier (`iparokenuniqueid`) attribute of the token to find
    @param owner, the owner (`iparokenowner`) attribute of the token to find
    @param no_members, if true this suppresses processing of membershib attributes
    @param all, retrieves all attributes
    @param raw, returns the raw response, only changes output format

    @return the request.Response from the otpoken_show request
    """

    method = 'otptoken_find'

    args = None

    if searchstring:
        args = searchstring

    params = {}

    if uniqueid is not None:
        params['ipatokenuniqueid'] = uniqueid

    if owner is not None:
        params['ipatokenowner'] = owner

    if no_members is not None:
        params['no_members'] = no_members

    if allattrs is not None:
        params['all'] = allattrs

    if raw is not None:
        params['raw'] = raw

    return self.request(
        method,
        args=args,
        params=params
    )

def otptoken_show(
        self,
        uniqueid: str,
        no_members: Union[bool, None]=None,
        allattrs: Union[bool, None]=None,
        raw: Union[bool, None]=None
):
    """
    @brief Complete implementation the otptoken_show request

    @param self The object
    @param uniqueid, the unique identifier (`iparokenuniqueid`) attribute of the token to show
    @param no_members, if true this suppresses processing of membershib attributes
    @param all, retrieves all attributes
    @param raw, returns the raw response, only changes output format

    @return the request.Response from the otpoken_show request
    """

    method = 'otptoken_show'

    args = uniqueid

    params = {}

    if no_members is not None:
        params['no_members'] = no_members

    if allattrs is not None:
        params['all'] = allattrs

    if raw is not None:
        params['raw'] = raw

    return self.request(
        method,
        args=args,
        params=params
    )
