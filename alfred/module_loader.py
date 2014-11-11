"""
Dynamic module loader

"""

import sys


class Loader:
    def __init__(self, path):
        sys.path.insert(0, path)

    def load_class(self, module_name, class_name):
        try:
            mod = self.load_mod(module_name)
            class_ = getattr(mod, class_name)
            return class_
        except ImportError:
            print 'can not load class %s' % str(class_name)

    @staticmethod
    def load_mod(module_name):
        try:
            if module_name in sys.modules:
                mod = reload(sys.modules[module_name])
            else:
                mod = __import__(module_name)
            return mod
        except ImportError:
            print 'can not load module %s' % str(module_name)
