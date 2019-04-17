"""
Some common utilities for the API
"""
from datetime import datetime
from typing import List


def delist(
    thedict: dict
):
    """
    @brief      Given a dictionary, check all the key values and if
                the value is a list, and the list has one item, then
                replace the list with the single item in the list

    @param      thedict  The dictionary to process

    @return     a dictionary with no single element lists
    """
    cleandict = {}
    timeformat = '%Y%m%d%H%M%SZ'
    for key in thedict:
        cleandict[key] = thedict[key]
        if isinstance(thedict[key], list):
            if len(thedict[key]) == 1:
                cleandict[key] = thedict[key][0]

        # Convert serialised datetime dicts back into a datetime object
        if isinstance(cleandict[key], dict):
            if '__datetime__' in cleandict[key]:
                cleandict[key] = datetime.strptime(
                    cleandict[key]['__datetime__'],
                    timeformat
                )

    return cleandict


def listdelist(
    thelist: List[dict]
):
    """
    @brief      Uses the delist functio on a list of Dictioaries

    @param      thelist  The list of dictionaries

    @return     a list of dictionaries with no single element lists
    """
    cleanlist = []
    for item in thelist:
        cleanlist.append(delist(item))

    return cleanlist
