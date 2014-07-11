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
from statistics import TestStatistics
import alfred


class TestFile(alfred.returncodes):
    def __init__(self, directory, filename):
        self.setup = None
        self.tests = None
        self.teardown = None
        self.config = {}
        self.stats = TestStatistics()
        self.filename = filename
        self.directory = directory

    def run(self):
        """execute the test"""
        return TestFile.SUCCESS

    def get_description(self):
        """return the description of the test"""
        return self.get(key='description', default='No Description Set')

    def get_name(self):
        """return the name of the test"""
        return self.get(key='name', default='No Name Set')

    def get(self, key=None, default=''):
        """returns the value of a key

        Arguments:
        key:    name of the key or the default value
        """
        if key is None:
            return self.config
        else:
            return self.config.get(key, default)

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


class Setup:
    def __init__(self, cfg):
        self.cfg = cfg

    def run(self):
        print self.cfg.get('name')


class TearDown:
    def __init__(self, cfg):
        self.cfg = cfg

    def run(self):
        print self.cfg.get('name')

setup_types = {
    'alfred': Setup
}

test_types = {
    'alfred': TestFile
}

teardown_types = {
    'alfred': TearDown
}
