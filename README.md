# pyfreeipa

Python module for accessing the FreeIPA/Red Hat Identity Manager API (a.k.a IPA)

This module does not do any exception handling, it want's you to handle exceptions.

# Usage

The following sample sets up a IPA API object with minimal configuration.

```python
from pyfreeipa.Api import Api

ipaapi = Api(
    host="ipa.example.org",
    username="ipauser",
    password="somethingsecret"
)

response = ipaapi.ping()

if response.ok:
    result = response.json()['result']
    print('Good: %s' & result['summary'])
else:
    print('Bad: %s' % response.status_code)
```

# Examples

The `pyfreeipa` module itself can be executed as a wrapper script around `pyfreeipa.Api`

# FreeIPA API Methods

The `Api` object supports both implemented and unimplemented methods

## Unimplemented Methods

Unimplemented methods are supported via the `Api.request()` method:

```python
ipaapi.request(
    method='group_add_member',
    args=['groupname'],
    parameters={
        'users': [
            'anne',
            'bob',
            'claire'
        ]
    }
)
```


## Implemented Methods

# Other Methods

The `Api` object has a some methods that do not directly relate to requests to the IPA API

## `login()`

## `get()`

## `post()`

## `put()`

## `request()`

## `warnings`

## `clearwarnings()`
