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
            protocol: str='https',
            verify_ssl: bool=True,
            verify_method: Union[bool, str]=True,
            verify_warnings: bool=True,
            version: str='2.228',
            dryrun: bool=False
    ):
        """
        @brief The initiator of the pyfreeipa.Api class

        @param self This object
        @param host The address of the IPA server
        @param username The username of the IPA user to connect to the IPA server
        @param password The password for the IPA user
        @param port The port to connect to (Default: 443)
        @param protocol The protocol to connect with (Default: https)
        @param verify_ssl If True then the TLS/SSL connection will verified as being secure and has valid certificates. (Default: True)
        @param verify_method Can be a True, False, or a string pointing to a certificate or directory holding certificaates. (Default: True)
        @param verify_warnings If True then TLS/SSL warnings will be emitted to stderr. (Default: True)
        @param version Used to over-ride the default IPA API version string. (Default: 2.228)
        @param dryrun If set to True this will stop any requests from making changes to the IPA directory (Default: False)
        """

        self._host = host
        self._username = username
        self._password = password
        self._port = port
        self._protocol = protocol
        self._verify_ssl = verify_ssl
        self._verify_method = verify_method
        self._verify_warnings = verify_warnings
        self._version = version
        self._dryrun = dryrun

        self.warnings = []

        if not self._verify_warnings:
            reason = (
                'Verifying TLS connection to %s disabled.' %
                self._host
            )
            self.warnings.append(reason)

        self._baseurl = (
            "%s://%s/ipa" %
            (
                self._protocol,
                self._host
            )
        )

        self._sessionurl = "%s/session/json" % self._baseurl
        self._loginurl = "%s/session/login_password" % self._baseurl

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
            'Referer': self._baseurl,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        self.login()

    def get(
            self,
            *dargs,
            **kwargs
    ):
        """
        @brief This exposes a raw get method for the session
        """
        response = self._session.get(
            *dargs,
            **kwargs
        )
        return response

    def post(
            self,
            *dargs,
            **kwargs
    ):
        """
        @brief This exposes a raw post method for the internal session
        """
        response = self._session.post(
            *dargs,
            **kwargs
        )
        return response

    def put(
            self,
            *dargs,
            **kwargs
    ):
        """
        @brief This exposes a raw put method for the internal session
        """
        response = self._session.put(
            *dargs,
            **kwargs
        )
        return response

    def request(
            self,
            method,
            args=None,
            params=None
    ):
        """
        @brief This cleans up the args and parameters posts the and handles the request
        and returns the response

        @param self This object
        @param method The FreeIPA API method to request
        @param args A list of arguments to be passed to the method request
        @param params A dictionary of parameters to be passed to the method request

        @return a requests.Response object
        """
        if args:
            if not isinstance(args, list):
                args = [args]
        else:
            args = []

        if not params:
            params = {}

        if self._version:
            params.setdefault('version', self._version)

        data = {
            'id': 0,
            'method': method,
            'params': [args, params]
        }

        response = self.post(
            self._sessionurl,
            data=json.dumps(data),
            verify=self._verify_ssl
        )

        return response

    def clearwarnings(self):
        """
        @brief      Retrieve and clear the warning array

        @param      self  The object

        @return     the warnings array before it was cleared
        """
        warnings = self.warnings
        self.warnings = []
        return warnings

# All definitions from this point are IPA API commands
# in alphabetical order (hopefully)

    def login(self):
        """
        @brief      Returns the response from the login command

        @param      self  The object

        @return     the requests.Response from the login request
        """
        logindata = {
            'user': self._username,
            'password': self._password
        }

        loginheaders = {
            'referer': self._loginurl,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        response = self.post(
            self._loginurl,
            data=logindata,
            headers=loginheaders
        )

        return response

    def ping(self):
        """
        @brief      Returns the response from the ping command

        @param      self  The object

        @return     the requests.Response from the ping request
        """
        return self.request('ping')

    def whoami(self):
        """
        @brief      Returns the response from the whoami command

        @param      self  The object

        @return     the requests.Response from the whoami request
        """
        return self.request('whoami')
