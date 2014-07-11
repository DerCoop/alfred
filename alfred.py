#!/usr/bin/env python
"""
Alfred is a test-suite for functional tests

you can use it as it is or create you own classes

"""
__author__ = 'coop'

import os
import logging as log


def parse_config(configfile):
    from alfred.config import AlfredConfig
    return AlfredConfig(configfile)


def create_statistics():
    from alfred.statistics import TestStatistics
    return TestStatistics()


def get_tests(test_dir, test_type):
    from alfred.testfile import types
    tests = []
    for root, dirs, files in os.walk(test_dir, topdown=False):
        for name in files:
            if name.endswith('.t'):
                tmp_test = types[test_type](root, name)
                if tmp_test.get_description() and tmp_test.get_name():
                    tmp_test.set('source', os.path.join(root, name))
                    tmp_test.set('test_dir', root)
                    tests.append(tmp_test)
    return tests


def main():
    from alfred.config import get_cli_options
    from alfred import returncodes
    import alfred.misc as misc
    try:
        from alfred.setup import types as setup_types
    except ImportError:
        from alfred import setup_types
    try:
        from alfred.teardown import types as teardown_types
    except ImportError:
        from alfred import teardown_types
    try:
        from alfred.testfile import types as test_types
    except ImportError:
        from alfred import test_types


    configfile = ''
    opts, args = get_cli_options()

    # configure logger
    # reset old log settings
    if log.root:
        del log.root.handlers[:]

    formatstring = '[%(levelname)s]: alfred: %(message)s'
    if opts.loglevel:
        loglevel = log.getLevelName(opts.loglevel.upper())
    else:
        loglevel = log.WARN

    log.basicConfig(format=formatstring, level=loglevel)

    # parse config
    if opts.config_file:
        configfile = opts.config_file

    if not os.path.isfile(configfile):
        msg = 'config file did not exist (' + configfile + ')'
        misc.die(-1, msg)

    # lets test
    cfg = parse_config(configfile)
    stats = create_statistics()

    test_type = cfg.get('test_type', 'alfred')
    setup_type = cfg.get('setup_type', 'alfred')
    teardown_type = cfg.get('teardown_type', 'alfred')

    # TODO setup
    setup = setup_types[setup_type](cfg)
    setup.run()

    tests = get_tests(cfg.get('test_dir'), test_type)
    for test in tests:
        test.run()
        rc = test.get('rc')
        stats.update(rc)
        if rc == returncodes.SUCCESS:
            log.info('\'%s\' finished successful' % test.get_name())
        elif rc == returncodes.SKIPPED:
            log.warn('\'%s\' skipped: %s' % (test.get_name(), test.get('skip')))
        elif rc == returncodes.FAILURE:
            log.error('\'%s\' failed at cmd(s) \'%s\'' % (test.get_name(), test.get('failed_cmd')))
            if cfg.get('stop_on_error') == "True":
                break
    # TODO Teardown
    teardown = teardown_types[teardown_type](cfg)
    teardown.run()

    stats.write()


if __name__ == '__main__':
    main()