"""
Process command line arguments and/or load configuration file
"""
import argparse
import sys
import os.path
from typing import Union
import yaml


class Configuration:
    """
    @brief      Class for configuration.
    """

    def __init__(self):
        """
        @brief      Constructs the object.

        @param      self  The object
        """

        # Set defaults
        defaults = {
            'ipaserver': {
                'host': 'ipaserver.example.org',
                'user': 'username',
                'password': None,
                'port': 443,
                'version': 2.228,
                'verify_ssl': True,
                'verify_method': True,
                'verify_warnings': True
            }
        }

        self.__dict__.update(defaults)

        args = self._do_args()

        # Override configuration defaults with values from the config file
        if os.path.isfile(args.file):
            with open(args.file, 'r') as configfile:
                self.__dict__.update(yaml.load(configfile))

        # Override configuration loaded from file with command line arguments
        # pylint: disable=maybe-no-member
        if args.server:
            self.ipaserver['host'] = args.server

        if args.user:
            self.ipaserver['user'] = args.user

        if args.password:
            self.ipaserver['password'] = args.password

        if args.port:
            self.ipaserver['port'] = args.port

        if args.version:
            self.ipaserver['version'] = args.version

        # This one can be bool or str values
        if args.verify_method is not None:
            self.ipaserver['verify_method'] = args.verify_method

        if args.verify_ssl is not None:
            self.ipaserver['verify_ssl'] = args.verify_ssl

        if args.verify_warnings is not None:
            self.ipaserver['verify_warnings'] = args.verify_warnings

        # If there's no config file, write one
        if not os.path.isfile(args.file):
            print(
                "The configuration file %s was missing,"
                " wrote default configuration to file" %
                args.file
            )
            with open(args.file, 'w') as configfile:
                yaml.dump(vars(self), configfile, default_flow_style=False)
            sys.exit(0)

        # Set state from command line
        self.command = args.command
        self.dryrun = args.dryrun

    @staticmethod
    def _do_args():
        """
        @brief      { function_description }

        @return     { description_of_the_return_value }
        """
        # Parse command line arguments and modify config
        parser = argparse.ArgumentParser(
            prog='pyfreeipa.py',
            description='Python FreeIPA tools'
        )

        # Command line arguments
        parser.add_argument(
            "-v",
            "--verbose",
            dest='verbose',
            help="Increase output to stderr and stdout",
            action="store_true"
        )

        parser.add_argument(
            "-q",
            "--quiet",
            dest='quiet',
            help="Reduce output to stderr and stdout",
            action="store_true"
        )

        parser.add_argument(
            "-d",
            "--dry_run",
            dest='dryrun',
            help="Do a dry run, no changes written to IPA server",
            action="store_true"
        )

        parser.add_argument(
            "-f",
            "--file",
            default='pyfreeipa.conf.yaml',
            dest='file',
            help="Specify a configuration file",
        )

        parser.add_argument(
            '-s',
            '--server',
            default=None,
            type=str,
            dest='server',
            help="Hostname of IPA server"
        )

        parser.add_argument(
            '-u',
            '--user',
            default=None,
            type=str,
            dest='user',
            help="The username used to connect to the IPA server"
        )

        parser.add_argument(
            '-p',
            '--password',
            default=None,
            type=str,
            dest='password',
            help="The password used to conenct to the IPA server"
        )

        parser.add_argument(
            '--port',
            default=None,
            type=str,
            dest='port',
            help="The password used to conenct to the IPA server"
        )

        parser.add_argument(
            '--version',
            default=None,
            type=str,
            dest='version',
            help="The IPA server API version"
        )

        parser.add_argument(
            '--verify_ssl',
            default=None,
            type=bool,
            dest='verify_ssl',
            help=(
                "If true the SSL certificate of the"
                " IPA server will be verified"
            )
        )

        parser.add_argument(
            '--verify_warnings',
            default=None,
            type=bool,
            dest='verify_warnings',
            help=(
                "If false warnings about the SSL state of "
                "the IPA server will be silenced"
            )
        )

        parser.add_argument(
            '--verify_method',
            default=None,
            type=Union[bool, str],
            dest='verify_method',
            help=(
                "The method used to validate the SSL state of "
                "the IPA server"
            )
        )

        # Positional commands
        parser.add_argument(
            dest='command',
            help='Command help',
            type=str,
            choices=[
                'dumpconfig',
                'connectiontest'
            ]
        )

        return parser.parse_args()
