""" Parse config file for alfred

    module for parsing the configuration and the command line interface arguments

    Written by DerCoop <dercoop@users.sourceforge.net>
    """

__author__ = 'coop'


import ConfigParser
import logging as log
import argparse


class AlfredConfig:
    """config class"""
    def __init__(self, configfile):
        self.config = {}
        self._parse_cfg(configfile)

    def _parse_cfg(self, fp):
        """parse stupid the whole config file

        Arguments:
        fp:     file-like object
        """
        config = ConfigParser.ConfigParser()
        config.readfp(fp)
        for section in config.sections():
            for key, value in config.items(section):
                self.set(key, value)

    def get(self, key, default=None):
        """returns the value of a key

        Arguments:
        key:     name of the key
        default: default value
        """
        return self.config.get(key, default)

    def set(self, key, value):
        """set a key

        Arguments:
        key:    name of the key to set
        value:  the value to set
        """
        self.config[key] = value


def get_cli_options():
    """returns a pair (values, args) of the command line options"""
    parser = argparse.ArgumentParser(description='test framework for functional tests')
    parser.add_argument('-C', '--configfile', action='store', type=argparse.FileType('r'),
                        default='cfg/config.ini',
                        help='the name of the configfile')

    parser.add_argument('-L', '--loglevel', action='store', default='warning',
                        choices=['critical', 'error', 'warning', 'info', 'debug', 'notset'],
                        help='set your loglevel, default = warning')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='print statistics verbose')
    parser.add_argument('-O', '--overwrite', action='store',
                        help='overwrite config options, comma separated key:value list '
                             '(key:value,key:value)')
    parser.add_argument('-F', '--filter', action='append', default=None, nargs='+',
                        help='RegEx filter options, the first argument must be the filter type '
                             '(n == name, d == directory [relative from the test-dir])')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='print logging to stdout')
    # TODO
    todo_config = parser.add_argument_group(title='ToDo',
                                            description='this arguments are not '
                                                        'completely implemented')
    todo_config.add_argument('--store-output', action='store', type=argparse.FileType('w'),
                             help='the name of the file where the output should be stored')
    todo_config.add_argument('-E', '--logfile', action='store', type=argparse.FileType('w'),
                             help='the name of the file where the output should be stored')

    return parser.parse_args()
