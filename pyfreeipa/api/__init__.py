"""
{ item_description }
"""
# import sys
# import urllib
import json
from typing import Union
import requests
# import pathlib
import urllib3


class Api:
    """
    @brief      Class for api connection to an IPA server.
    """
    def __init__(
            self,
            host: type=str,
            username: type=str,
            password: type=str,
            port: int=443,
            verify_ssl: bool=True,
            verify_method: bool=True,
            verify_warnings: bool=True,
            dryrun: bool=False
    ):

        self._host = host
        self._username = username
        self._password = password
        self._port = port
        self._verify_ssl = verify_ssl
        self._verify_method = verify_method
        self._verify_warnings = verify_warnings
        self._dryrun = dryrun

        self.warnings = []

        if not self._verify_warnings:
            reason = (
                'Verifying TLS connection to %s disabled.' %
                self._host
            )
            self.warnings.append(reason)

        self._baseurl = (
            "https://%s:%s/ipa" %
            (
                self._host,
                self._port
            )
        )

        if not self._verify_warnings:
            reason = (
                "TLS warnings from %s disabled" %
                self._host
            )
            self.warnings.append(reason)
            urllib3.disable_warnings()

        self._session = requests.Session()
        self._session.url = self._baseurl
        self._session.verify = self._verify_ssl
        self._session.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain'
        }
        self._session.auth = requests.auth.HTTPBasicAuth(
            self._username,
            self._password
        )

    def _get(
            self,
            commandurl: type=str,
            params: Union[None, dict]=None
    ):
        print(commandurl)
        response = self._session.get(
            url=commandurl,
            params=params
        )
        return response

    def _post(
            self,
            commandurl: type=str,
            data: type=dict,
            headers: Union[None, dict]=None,
    ):
        if headers:
            response = self._session.post(
                url=commandurl,
                data=json.dumps(data),
                headers=headers
            )
        else:
            response = self._session.post(
                url=commandurl,
                data=json.dumps(data)
            )
        return response

    def login(self):
        """
        Logs in to freeIPA
        """

        commandurl = (
            "%s/session/login_password" %
            self._baseurl
        )
        data = {
            'user': self._username,
            'password': self._password
        }
        headers = {
            'referer': commandurl,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain'
        }
        response = self._session.post(
            commandurl,
            data=data,
            headers=headers
        )
        return response

    def clearwarnings(self):
        """
        @brief      Clears the warning array

        @param      self  The object

        @return     Returns the cleared warnings array
        """
        self.warnings = []
        return self.warnings
