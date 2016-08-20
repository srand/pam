import sys
import os
import imp


class Loader(object):
    def __init__(self, package, path):
        self.package = package
        self.path = path
        sys.modules[self.package] = imp.new_module(self.package)

    def load(self):
        if os.path.isfile(self.path):
            self.load_file(self.path)
            return
        for root, dirs, files in os.walk(self.path):
            for file in files:
                fullpath = os.path.join(root, file)
                self.load_file(fullpath)

    def load_file(self, path):
        file = os.path.basename(path)
        base, ext = os.path.splitext(file)
        if ext == ".py":
            with open(path) as fd:
                imp.load_module("{}.{}".format(self.package, base), fd, path, ('.py', 'r', imp.PY_SOURCE))


class Dispatch(object):
    def __init__(self):
        self.typemap = {}
        self.default = None
        
    def __call__(self, *args):
        types = tuple(arg.__class__ for arg in args)
        function = self.typemap.get(types)
        if function is None:
            function = self.default
        if function is None:
            raise TypeError("no match")
        return function(*args)

    def add_method(self, types, function):
        if types in self.typemap:
            raise TypeError("duplicate registration of method")
        self.typemap[types] = function

    def add_default_method(self, function):
        if self.default is not None:
            raise TypeError("duplicate registration of default method")
        self.default = function


def multidispatch(dispatch, *types):
    def register(function):
        if len(types) > 0:
            dispatch.add_method(types, function)
        else:
            dispatch.add_default_method(function)
        return dispatch
    return register
