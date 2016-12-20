#!/usr/bin/env python3
"""
Alfred is a test-suite for functional tests

you can use it as it is or create you own classes

Return:
0 on success,
1 if at least one test are broken or were skipped

"""
__author__ = 'coop'

import os
import sys
import logging as log


def parse_config(configfile):
    from alfred.config import AlfredConfig
    return AlfredConfig(configfile)


def create_statistics():
    from alfred.statistics import TestStatistics
    return TestStatistics()


def filter_test(test, test_filters):
    '''document me
        :param test: the test to check
        :type test: TestClass()
        :param test_filters: the filter for the test
        :type test_filters: list of tuples with type and value
        :return:
        :rtype:
        '''
    import alfred.misc as misc
    import re

    if not test_filters:
        return True

    for test_filter in test_filters:
        if len(test_filter) < 2:
            misc.die(1, 'Filter option needs at least 2 arguments: '
                        'filter type and filter value')
        filter_type = test_filter[0]
        if filter_type == 'd':
            # filter by directory
            log.info('filter by directory %s, test_dir %s' % (test_filter[1:],
                                                              test.test_dir))
            for directory in test_filter[1:]:
                if os.path.normpath(test.test_dir) == \
                        os.path.normpath(directory):
                    return True
        elif filter_type == 'n':
            # filter by test name
            log.info('filter by test-name %s, test.name %s' % (test_filter[1:],
                                                               test.name))
            for name in test_filter[1:]:
                # check if the filter is an part of the testname
                if re.search(name, test.name):
                    return True
        elif filter_type == 'alfred':
            # build in filters
            if test_filter[1] == 'smoke':
                return test.cfg.get('smoke', None) == 'True'
        else:
            misc.die(1, 'unknown filter type %s' % filter_type)

    return False


def get_tests(test_dir, test_module, test_class, cfg, test_filter=None):
    import alfred.module_loader as module_loader
    import alfred.misc as misc
    loader = module_loader.Loader(cfg.get('module_path', default='alfred'))
    test_module = loader.load_class(test_module, test_class)
    git_root = misc.get_git_root()

    tests = []
    for tdir in test_dir.split():
        for root, dirs, files in os.walk(tdir, topdown=False):
            for name in files:
                if name.endswith('.t'):
                    log.info('found %s' % name)
                    tmp_test = test_module(root, name)
                    if tmp_test.description and tmp_test.name:
                        tmp_test.source = os.path.normpath(os.path.join(root,
                                                                        name))
                        tmp_test.test_dir = root
                        tmp_test.working_dir = os.path.normpath(
                            os.path.join(git_root, cfg.get('working_dir',
                                                           root))
                        )
                        tmp_test.root_cfg = cfg
                        if filter_test(tmp_test, test_filter):
                            log.debug('add test %s',
                                      os.path.normpath(
                                          os.path.join(tmp_test.test_dir,
                                                       tmp_test.name)
                                      )
                            )
                            tests.append(tmp_test)
    return tests


def main():
    from alfred.config import get_cli_options
    from alfred import returncodes
    from alfred import bcolors
    import alfred.misc as misc
    import alfred.module_loader as module_loader
    import time

    opts = get_cli_options()

    # configure logger
    if log.root:
        del log.root.handlers[:]

    formatstring = '[%(levelname)s]: alfred: %(message)s'
    loglevel = log.getLevelName(opts.loglevel.upper())

    # capture warnings to logging
    # https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
    log.captureWarnings(True)

    test_filter = opts.filter

    # parse config
    configfile = opts.configfile

    cfg = parse_config(configfile)
    if opts.overwrite:
        for option in opts.overwrite.split(','):
            key, value = option.split(':')
            cfg.set(key, value)

    logfile = cfg.get('logfile')
    working_dir = cfg.get('working_dir')
    git_root = misc.get_git_root()
    if working_dir:
        if git_root:
            working_dir = os.path.normpath(os.path.join(git_root, working_dir))

    if not opts.debug and logfile and working_dir:
        try:
            os.makedirs(working_dir)
        except OSError as ex:
            # file exists
            #print ex
            pass
        logfile = os.path.normpath(os.path.join(working_dir, logfile))
        # remove the main logfile if there is an old version
        try:
            os.remove(logfile)
        except OSError as ex:
            # the file did not exist
            pass
        # create the base path of the logfile
        try:
            os.makedirs(os.path.dirname(logfile))
        except OSError as ex:
            # directory already exists
            pass
        log.basicConfig(format=formatstring, level=loglevel, filename=logfile)
    else:
        log.basicConfig(format=formatstring, level=loglevel)

    stats = create_statistics()

    test_module = cfg.get('test_module', default='alfred')
    test_class = cfg.get('test_class', default='TestClass')
    setup_class = cfg.get('setup_class', default='SetupClass')
    teardown_class = cfg.get('teardown_class', default='TearDownClass')
    loader = module_loader.Loader(cfg.get('module_path', default='alfred'))

    log.debug('get tests')
    tests = get_tests(cfg.get('test_dir', default='examples'), test_module, test_class, cfg,
                      test_filter)
    if not tests:
        misc.die(0, 'no tests found')

    if opts.sorted:
        tests.sort(key=lambda elem: elem.source)
    elif opts.random:
        import random
        random.shuffle(tests)

    log.debug('setup tests')
    setup_module = loader.load_class(test_module, setup_class)
    setup = setup_module(cfg)
    setup.run()

    main_start_time = 0
    # lets test
    try:
        print('run tests\n')
        main_start_time = time.time()
        for test in tests:
            sys.stdout.write('* %-50s ' % test.name)
            sys.stdout.flush()
            start_time = time.time()
            test.run()
            rc = test.rc
            stats.update(rc, name=test.name)
            if rc == returncodes.SUCCESS:
                log.info('\'%s\' finished successful' % test.name)
                sys.stdout.write(bcolors.BLUE + 'OK\t\t' + bcolors.ENDC)
            elif rc == returncodes.SKIPPED:
                log.warn('\'%s\' skipped: %s' % (test.name, test.skip))
                sys.stdout.write(bcolors.YELLOW + 'SKIPPED\t' + bcolors.ENDC)
            elif rc == returncodes.FAILURE:
                log.error('\'%s\' failed at cmd(s) \'%s\'' % (test.name, test.failed_command))
                if cfg.get('stop_on_error') == "True":
                    break
                sys.stdout.write(bcolors.RED + 'FAIL\t' + bcolors.ENDC)
            end_time = time.time()
            print(' in %f s' % (end_time - start_time))

    except KeyboardInterrupt:
        log.debug('aborted by user')
    finally:
        print('')
        main_end_time = time.time()
        log.debug('teardown tests')
        teardown_module = loader.load_class(test_module, teardown_class)
        teardown = teardown_module(cfg)
        teardown.run()

        if opts.verbose:
            stats.write_verbose()
        else:
            stats.write()
        print('test time: %f s' % (main_end_time - main_start_time))

    if stats.all_success():
        print('All tests finished successful')
        sys.exit(0)
    elif stats.get(returncodes.FAILURE):
        misc.die(1, 'At least one test is broken')
    else:
        log.warn('At least one test is skipped')
        sys.exit(0)

if __name__ == '__main__':
    main()

