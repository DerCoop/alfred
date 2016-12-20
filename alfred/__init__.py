class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


class returncodes:
    FAILURE = 'failed'
    SUCCESS = 'success'
    SKIPPED = 'skipped'


# define default classes
from alfred.statistics import TestStatistics
import os


class TestClass(returncodes):
    def __init__(self, directory, filename):
        self.source = os.path.join(directory, filename)

        self.__config = self._parse_cfg(self.source, 'main')
        self.__stats = TestStatistics()
        self.__filename = filename
        self.__directory = directory

        self.__rc = TestClass.SKIPPED
        self.__name = self.__config.get('name', 'No Name Set')
        self.__description = self.__config.get('description',
                                               'No Description Set')
        self.__source = None

        self.__test_dir = None
        self.__working_dir = None
        self.__root_cfg = None
        self.__failed_command = 'not set'
        self.__skip = None

    @property
    def failed_command(self):
        """return the failed command"""
        return self.__failed_command

    @failed_command.setter
    def failed_command(self, command):
        """set the failed command"""
        self.__failed_command = command

    @property
    def description(self):
        """return the description of the test"""
        return self.__description

    @description.setter
    def description(self, value):
        """set the description of the test"""
        self.__description = value

    @property
    def name(self):
        """return the name of the test"""
        return self.__name

    @name.setter
    def name(self, value):
        """set the name of the test"""
        self.__name = value

    @property
    def rc(self):
        """return the return code of the test"""
        return self.__rc

    @rc.setter
    def rc(self, value):
        """set the return code of the test"""
        self.__rc = value

    @property
    def source(self):
        """return the sourcefilename including the path"""
        return self.__source

    @source.setter
    def source(self, value):
        """set the sourcefile"""
        self.__source = value

    @property
    def test_dir(self):
        """return the test directory path"""
        return self.__test_dir

    @test_dir.setter
    def test_dir(self, value):
        """set the test directory"""
        self.__test_dir = value

    @property
    def working_dir(self):
        """return the working directory path"""
        return self.__working_dir

    @working_dir.setter
    def working_dir(self, value):
        """set the working directory"""
        self.__working_dir = value

    @property
    def root_cfg(self):
        """return the root config"""
        return self.__root_cfg

    @root_cfg.setter
    def root_cfg(self, value):
        """set the root config"""
        self.__root_cfg = value

    @property
    def skip(self):
        """return the skip message"""
        return self.__skip

    @skip.setter
    def skip(self, message):
        """set the skip message"""
        self.__skip = message

    @staticmethod
    def _parse_cfg(filename, section):
        """parse stupid the whole config file

        Arguments:
        filename:   filename
        section:    the section to parse

        Return:
        dictionary with all key-value pairs (or empty)
        """
        # TODO validate the testfile
        import ConfigParser
        cfg = {}
        config = ConfigParser.ConfigParser()
        config.read(filename)
        if not config.has_section(section):
            return
        for key, value in config.items(section):
            cfg[key] = value
        return cfg

    def __check_skip(self):
        """check if the test is skipped

            Note: set the var somewhere
        """
        if self.skip:
            return True
        else:
            return False

    def run(self):
        """execute the test"""
        self.rc = TestClass.SUCCESS

        if self.__check_skip():
            return

        return

    def get(self, key=None, default=''):
        """returns the value of a key

        Arguments:
        key:    name of the key or the default value
        """
        if key is None:
            return self.__config
        else:
            return self.__config.get(key, default)

    def set(self, key, value):
        """set a key

        Arguments:
        key:    name of the key to set
        value:  the value to set
        """
        self.__config[key] = value

    def append(self, key, value):
        """append a value to a key

        if the key did not exist, it will created

        Arguments:
        key:    name of the key to set
        value:  the value to set
        """
        if self.__config.has_key(key):
            self.__config[key].append(value)
        else:
            self.__config[key] = [value]


class SetupClass:
    def __init__(self, cfg):
        self.cfg = cfg

    def run(self):
        print('setup: %s' % self.cfg.get('name'))


class TearDownClass:
    def __init__(self, cfg):
        self.cfg = cfg

    def run(self):
        print('teardown: %s' % self.cfg.get('name'))
