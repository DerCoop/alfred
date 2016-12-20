""" misc functions

    Written by DerCoop <dercoop@users.sourceforge.net>
    """

__author__ = 'coop'


import sys
import logging as log


def die(rc, message):
    """print message and exit

    Arguments:
    rc:         returncode
    message:    log message
    """
    log.error(message)
    sys.exit(rc)


def grep(fname, regex):
    """implementation of unix grep

    args:
    fname:  the name of the file which will be scanned
    regex:  the regular expression of the searchstring

    return:
    all matching lines

    """
    import re

    result = ''
    try:
        with open(fname, 'r') as fd:
            for line in fd:
                if re.search(regex, line):
                    if not line == None:
                        result += line
        return result
    except:
        raise


def get_bool_from_string(string):
    """convert a string to a boolean

    Arguments:
    string: the string to convert

    Return:
    True if the string is in 'true_values' (not case sensitive!)
    else False
    """
    _true_values_ = ['yes', 'y', 'true', 't', '1']
    return string.lower() in _true_values_


def is_debug():
    """get the current loglevel

    return:
    True if the loglevel is Debug
    False else
    """
    if get_loglevel() <= log.DEBUG:
        return True
    return False


def get_loglevel():
    """returns the current loglevel"""
    return log.getLogger().getEffectiveLevel()


def get_git_root():
    """return the root of the current git"""
    import subprocess
    cmd = ['git', 'rev-parse', '--show-toplevel']
    return str(subprocess.check_output(cmd).strip())
