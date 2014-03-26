"""testfiles class

    Main definition of the missions from the files

    Written by DerCoop <dercoop@users.sourceforge.net>
    """

__author__ = 'coop'


import subprocess
import alfred
import shlex
import ConfigParser
from alfred.statistics import TestStatistics
import logging as log


class TestFile(alfred.returncodes):
    def __init__(self, filename):
        self.setup = None
        self.tests = None
        self.teardown = None
        self.config = {}
        self._parse_file(filename)
        self.stats = TestStatistics()

    def _parse_file(self, filename):
        """parse stupid the whole file

        Arguments:
        filename:   fqn of the configfile
        """
        config = ConfigParser.ConfigParser()
        config.read(filename)
        for section in config.sections():
            if section == 'main':
                for key, value in config.items(section):
                    self.set(key, value)
            elif section == 'setup':
                for key, value in config.items(section):
                    if key == 'cmd':
                        self.setup = value
            elif section == 'teardown':
                for key, value in config.items(section):
                    if key == 'cmd':
                        self.teardown = value
            elif section == 'test':
                for key, value in config.items(section):
                    if key == 'cmd':
                        self.tests = value
            else:
                log.warning('unknown section: %s' % str(section))

    def get(self, key=None):
        """returns the value of a key

        Arguments:
        key:    name of the key
        """
        if key == None:
            return self.config
        else:
            return self.config.get(key, None)

    def set(self, key, value):
        """set a key

        Arguments:
        key:    name of the key to set
        value:  the value to set
        """
        self.config[key] = value

    def append(self, key, value):
        """append a value to a key

        if the key did not exist, it will created

        Arguments:
        key:    name of the key to set
        value:  the value to set
        """
        if self.config.has_key(key):
            self.config[key].append(value)
        else:
            self.config[key] = [value]

    def run(self):
        """run the tests

        if the "skip" flag is not set, all tests from 'setup', 'test' and 'teardown'
        were executed. If there is an error at 'setup' or 'test', it will raise an exception
        and 'teardown' will executed! With the 'stop_on_error' flag, it is possible to run
        all tests without raising an exception
        At the 'teardown' section, there is no errorhandling, errors were only logged
        """
        if self.get('skip'):
            self.set('rc', TestFile.SKIPPED)
            return
        self.set('rc', TestFile.SUCCESS)
        try:
            self._setup()
            self._test()
        except:
            self.set('rc', TestFile.FAILURE)
        finally:
            self._teardown()
        return

    def _execute_cmd(self, cmd):
        """execute a command

        set the internal statistics and return 'failure' on failure or nothing on success

        Arguments:
        cmd:    the command to check
        """
        try:
            subprocess.check_call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            self.stats.update(TestFile.FAILURE)
            log.error('cmd \'%s\' failed', cmd)
            self.append('failed_cmd', cmd)
            return TestFile.FAILURE
        self.stats.update(TestFile.SUCCESS)
        return

    def _run_cmds(self, cmdlist):
        """run a list of commands

        If the 'stop_on_error' flag is True, this method will break at the first error

        Arguments:
        cmdlist:    a list with all commands to execute (commands are strings)
        """
        rc = TestFile.SUCCESS
        for cmd in cmdlist:
            cmd = shlex.split(cmd)
            ret = self._execute_cmd(cmd)
            if ret:
                rc = TestFile.FAILURE
                if self.get('stop_on_error') == 'True':
                    break
        return rc

    def _setup(self):
        """run all setup commands"""
        if not self.setup:
            log.warn('%s setup: nothing to do' % self.get('name'))
            return
        ret = self._run_cmds(str(self.setup).split('\n'))
        if not ret == TestFile.SUCCESS:
            raise

    def _test(self):
        """run all tests"""
        if not self.tests:
            log.warn('%s test: nothing to do' % self.get('name'))
            return
        ret = self._run_cmds(str(self.tests).split('\n'))
        if not ret == TestFile.SUCCESS:
            raise

    def _teardown(self):
        """run all teardown commands"""
        # no error handling
        if not self.teardown:
            log.warn('%s reardown: nothing to do' % self.get('name'))
            return
        return self._run_cmds(str(self.teardown).split('\n'))
