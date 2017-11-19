##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


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

    def add(self, types, function):
        if types in self.typemap:
            raise TypeError("duplicate registration of method")
        self.typemap[types] = function

    def set_default(self, function):
        if self.default is not None:
            raise TypeError("duplicate registration of default method")
        self.default = function


def multidispatch(dispatch, *types):
    def register(function):
        if len(types) > 0:
            dispatch.add(types, function)
        else:
            dispatch.set_default(function)
        def _call(*args):
            types = tuple(arg.__class__ for arg in args[1:])
            function = dispatch.typemap.get(types)
            if function is None:
                function = dispatch.default
            if function is None:
                raise TypeError("no match")
            return function(*args)
        return _call

    return register


class DepfileParser:
    def __init__(self, filename):
        self.data = ""
        self.product = ""
        self.dependencies = []

        if not os.path.exists(filename):
            return

        with open(filename) as f:
            self.data = f.read()

        self.data = self.data.replace("\n", "")
        self.data = self.data.replace("\r", "")
        self.data = self.data.replace("\\", "")

        index = self.data.find(":")
        if index < 0:
            return

        self.data = self.data[index+1:]
        self.product = self.data[0:index]
        self.dependencies = [dep for dep in self.data.split(" ") if dep]
        self.dependencies = [os.path.normpath(dep) for dep in self.dependencies]
