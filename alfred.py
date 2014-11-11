#!/usr/bin/env python
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


def filter_test(name, test_filter):
    import re
    if not test_filter:
        return True
    if re.search(test_filter, name):
        return True
    else:
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
                    if not filter_test(name, test_filter):
                        raise NotImplementedError
                    tmp_test = test_module(root, name)
                    if tmp_test.description and tmp_test.name:
                        tmp_test.source = os.path.join(root, name)
                        tmp_test.test_dir = root
                        tmp_test.working_dir = os.path.join(git_root, cfg.get('working_dir', root))
                        tmp_test.root_cfg = cfg
                        log.debug('add test %s', tmp_test.name)
                        tests.append(tmp_test)
    return tests


def main():
    from alfred.config import get_cli_options
    from alfred import returncodes
    import alfred.misc as misc
    import alfred.module_loader as module_loader

    opts = get_cli_options()

    # configure logger
    if log.root:
        del log.root.handlers[:]

    formatstring = '[%(levelname)s]: alfred: %(message)s'
    loglevel = log.getLevelName(opts.loglevel.upper())

    test_filter = opts.filter

    # parse config
    configfile = opts.configfile

    cfg = parse_config(configfile)
    log.basicConfig(format=formatstring, level=loglevel, filename=logfile)

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

    log.debug('setup tests')
    setup_module = loader.load_class(test_module, setup_class)
    setup = setup_module(cfg)
    setup.run()

    # lets test
    try:
        log.debug('run tests')
        for test in tests:
            test.run()
            rc = test.rc
            stats.update(rc, name=test.name)
            if rc == returncodes.SUCCESS:
                log.info('\'%s\' finished successful' % test.name)
            elif rc == returncodes.SKIPPED:
                log.warn('\'%s\' skipped: %s' % (test.name, test.skip))
            elif rc == returncodes.FAILURE:
                log.error('\'%s\' failed at cmd(s) \'%s\'' % (test.name, test.failed_command))
                if cfg.get('stop_on_error') == "True":
                    break
    except KeyboardInterrupt:
        log.debug('aborted by user')
    finally:
        log.debug('teardown tests')
        teardown_module = loader.load_class(test_module, teardown_class)
        teardown = teardown_module(cfg)
        teardown.run()

        if opts.verbose:
            stats.write_verbose()
        else:
            stats.write()

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

