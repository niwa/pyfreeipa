#!/usr/bin/env python

"""
Install module
"""

from distutils.core import setup

setup(
    name="PyFreeIPA",
    description="Python FreeIPA API interface",
    author="Aaron Hicks",
    author_email="aethylred@gmail.com",
    version="0.1.0",
    packages=[
        'pyfreeipa',
        'pyfreeipa.Api',
        'pyfreeipa.configuration'
    ],
    data_files=[('test', ['test/test_README.md'])],
    license='Apache 2.0',
    long_description=open('README.md').read(),
)
