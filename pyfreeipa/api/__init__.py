"""
{ item_description }
"""
import requests
import urllib
# import pathlib
import json
from typing import Union
import urllib3
import sys

class Api(object):
    """
    @brief      Class for api.
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
        dry_run: bool=False
    ):
        print("Does nothing")
