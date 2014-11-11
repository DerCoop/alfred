""" statistics class

    use this class to count the testcases and create statistics about
    with the return codes of the tests
    This class is also for the sub-test statistics

    Written by DerCoop <dercoop@users.sourceforge.net>
    """

__author__ = 'coop'


class TestStatistics():
    from alfred import returncodes
    SUCCESS = returncodes.SUCCESS
    FAILED = returncodes.FAILURE
    SKIPPED = returncodes.SKIPPED
    COUNTER = 'counter'

    def __init__(self):
        self.counter = 0
        self.success = 0
        self.failed = 0
        self.skipped = 0
        self._broken_tests = []
        self._skipped_tests = []

    def _add_broken_test(self, name):
        """add the name of the broken test to a list

        Arguments:
        name:   the name of the broken test
        """
        self._broken_tests.append(str(name))

    def _add_skipped_test(self, name):
        """add the name of a skipped test to a list

        Arguments:
        name:   the name of the skipped test
        """
        self._skipped_tests.append(str(name))

    def _get_broken_tests(self):
        """return a list with the names of all broken tests"""
        return self._broken_tests

    def _get_skipped_tests(self):
        """return a list with the names of all skipped tests"""
        return self._skipped_tests

    def update(self, counter, name=None):
        """increase the testcounter and the statistic counter for the returnvalue

        Arguments:
        counter:    the statistic counter to update
        """
        self.counter += 1
        if counter == TestStatistics.SUCCESS:
            self.success += 1
        elif counter == TestStatistics.FAILED:
            self.failed += 1
            if name:
                self._add_broken_test(name)
        elif counter == TestStatistics.SKIPPED:
            self.skipped += 1
            if name:
                self._add_skipped_test(name)

    def get(self, counter):
        """returns the current stand of an counter

        Arguments:
        counter:    the counter to get
        """
        if counter == TestStatistics.SUCCESS:
            return self.success
        elif counter == TestStatistics.FAILED:
            return self.failed
        elif counter == TestStatistics.SKIPPED:
            return self.skipped
        elif counter == TestStatistics.COUNTER:
            return self.counter

    def write(self):
        """write out the whole statistic"""
        from alfred import bcolors

        print('\nsummary:\n--------\n')
        print(bcolors.BLUE + 'success:\t%s' % self.get(TestStatistics.SUCCESS))
        print(bcolors.RED + 'failed: \t%s' % self.get(TestStatistics.FAILED))
        print(bcolors.YELLOW + 'skipped:\t%s' % self.get(TestStatistics.SKIPPED))
        print(bcolors.ENDC)
        print('executed tests:\t%s\n' % self.get(TestStatistics.COUNTER))

    def write_verbose(self):
        """write which tests are broken or skipped"""
        from alfred import bcolors

        # TODO expand for reasons
        if self.failed != 0:
            print(bcolors.RED + 'failed tests:')
            for test in self._get_broken_tests():
                print('\t%s' % str(test))
            print('\n')

        if self.skipped != 0:
            print(bcolors.YELLOW + 'skipped tests:')
            for test in self._get_skipped_tests():
                print('\t%s' % str(test))
            print('\n')

        print('\n')
        self.write()

    def all_success(self):
        """return True if all tests executed successful"""
        return self.counter == self.success


# vim: ft=py:tabstop=4:et