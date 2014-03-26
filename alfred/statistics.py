""" statistics class

    use this class to count the testcases and create statistics about
    with the return codes of the tests
    This class is also for the sub-test statistics

    Written by DerCoop <dercoop@users.sourceforge.net>
    """

__author__ = 'coop'


class TestStatistics():
    SUCCESS = 'success'
    FAILED = 'failed'
    SKIPPED = 'skipped'
    COUNTER = 'counter'

    def __init__(self):
        self.counter = 0
        self.success = 0
        self.failed = 0
        self.skipped = 0

    def update(self, counter):
        """increase the testcounter and the statistic counter for the returnvalue

        Arguments:
        counter:    the statistic counter to update
        """
        self.counter += 1
        if counter == TestStatistics.SUCCESS:
            self.success += 1
        elif counter == TestStatistics.FAILED:
            self.failed += 1
        elif counter == TestStatistics.SKIPPED:
            self.skipped += 1

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

        print '\nsummary:\n--------\n'
        print bcolors.BLUE + 'success:\t%s' % self.get(TestStatistics.SUCCESS)
        print bcolors.RED + 'failed: \t%s' % self.get(TestStatistics.FAILED)
        print bcolors.YELLOW + 'skipped:\t%s' % self.get(TestStatistics.SKIPPED)
        print bcolors.ENDC
        print 'executed tests:\t%s\n' % self.get(TestStatistics.COUNTER)


# vim: ft=py:tabstop=4:et