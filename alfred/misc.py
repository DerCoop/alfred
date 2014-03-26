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
