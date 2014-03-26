""" Parse config file for alfred

    module for parsing the configuration and the command line interface arguments

    Written by DerCoop <dercoop@users.sourceforge.net>
    """

__author__ = 'coop'


import ConfigParser
import optparse
import logging as log


class AlfredConfig:
    """config class"""
    def __init__(self, filename):
        self.config = {}
        self._parse_cfg(filename)

    def _parse_cfg(self, filename):
        """parse stupid the whole config file

        Arguments:
        filename:   fqn of the configfile
        """
        config = ConfigParser.ConfigParser()
        config.read(filename)
        for section in config.sections():
            for key, value in config.items(section):
                self.set(key, value)

    def get(self, key):
        """returns the value of a key

        Arguments:
        key:    name of the key
        """
        return self.config.get(key, None)

    def set(self, key, value):
        """set a key

        Arguments:
        key:    name of the key to set
        value:  the value to set
        """
        self.config[key] = value


def get_cli_options():
    """returns a pair (values, args) of the command line options"""
    parser = optparse.OptionParser(usage=optparse.SUPPRESS_USAGE)
    parser.add_option('--loglevel', action='store',
                      help='<critical | error | warning | info | debug | notset>')
    parser.add_option('--config-file', action='store',
                      help='the name of the configfile')

    return parser.parse_args()