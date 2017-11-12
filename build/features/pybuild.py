##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


from build.feature import Feature
from build.model import CXXLibrary
import os


class _PyBuildCustomCFlag(Feature):
    def __init__(self, str):
        super(_PyBuildCustomCFlag, self).__init__()
        self.str = str

    def transform(self, project, cxx_project, toolchain, **kwargs):
        cxx_project.add_cflag(self.str)


class PyBuildCustomCFlag(_PyBuildCustomCFlag):
    C89 = _PyBuildCustomCFlag("-std=c89")
    C99 = _PyBuildCustomCFlag("-std=c99")
    C11 = _PyBuildCustomCFlag("-std=c11")


class _PyBuildCustomCXXFlag(Feature):
    def __init__(self, str):
        super(_PyBuildCustomCXXFlag, self).__init__()
        self.str = str

    def transform(self, project, cxx_project, toolchain, **kwargs):
        cxx_project.add_cxxflag(self.str)


class PyBuildCustomCXXFlag(_PyBuildCustomCXXFlag):
    CXX11 = _PyBuildCustomCXXFlag("-std=c++11")
    CXX14 = _PyBuildCustomCXXFlag("-std=c++14")
    CXX17 = _PyBuildCustomCXXFlag("-std=c++17")
        

class PyBuildCustomLinkerFlag(Feature):
    def __init__(self, str):
        super(PyBuildCustomLinkerFlag, self).__init__()
        self.str = str

    def transform(self, project, cxx_project, toolchain, **kwargs):
        cxx_project.add_linkflag(self.str)


class _PyBuildOptimize(Feature):
    def __init__(self, levels):
        super(_PyBuildOptimize, self).__init__()
        self.levels = levels

    def transform(self, project, cxx_project, toolchain, **kwargs):
        if 'level' not in kwargs:
            raise ValueError('no "level" argument provided to optimize feature')
        if kwargs['level'] not in self.levels:
            raise ValueError('illegal "level" argument provided to optimize feature')
        value = self.levels[kwargs.get('level')]
        cxx_project.add_cflag(value)
        cxx_project.add_cxxflag(value)


class PyBuildOptimize:
    MSVC = _PyBuildOptimize({'disable': '/Od', 'space': '/Os', 'speed': '/Ot', 'full': '/Ox'})
    GNU = _PyBuildOptimize({'disable': '-O0', 'space': '-O1', 'speed': '-O2', 'full': '-O3'})


class _PyBuildProjectMacros(Feature):
    def __init__(self, prefix):
        super(_PyBuildProjectMacros, self).__init__()
        self.prefix = prefix

    def transform(self, project, cxx_project, toolchain, **kwargs):
        def key_value(key, value):
            return "{}".format(key) if value is None else "{}={}".format(key, value)
        for macro in project.get_macros(toolchain, inherited=True):
            flag = '{}{}'.format(self.prefix, key_value(macro.key, macro.value))
            cxx_project.add_cflag(flag)
            cxx_project.add_cxxflag(flag)

class PyBuildProjectMacros:
    GNU = _PyBuildProjectMacros('-D')
    MSVC = _PyBuildProjectMacros('/D')



class _PyBuildProjectIncPaths(Feature):
    def __init__(self, prefix):
        super(_PyBuildProjectIncPaths, self).__init__()
        self.prefix = prefix

    def transform(self, project, cxx_project, toolchain, **kwargs):
        for path in project.get_incpaths(toolchain, inherited=True):
            cxx_project.add_cflag('{}{}'.format(self.prefix, path.path))
            cxx_project.add_cxxflag('{}{}'.format(self.prefix, path.path))


class PyBuildProjectIncPaths:
    MSVC = _PyBuildProjectIncPaths('/I')
    GNU = _PyBuildProjectIncPaths('-I')


class _PyBuildProjectLibraries(Feature):
    def __init__(self, prefix):
        super(_PyBuildProjectLibraries, self).__init__()
        self.prefix = prefix

    def transform(self, project, cxx_project, toolchain, **kwargs):
        for lib in project.get_libraries(toolchain, inherited=True):
            cxx_project.add_library(self.prefix.format(name=lib.name))


class PyBuildProjectLibraries:
    MSVC = _PyBuildProjectLibraries('{name}')
    GNU = _PyBuildProjectLibraries('{name}')


class _PyBuildProjectLibPaths(Feature):
    def __init__(self, prefix):
        super(_PyBuildProjectLibPaths, self).__init__()
        self.prefix = prefix

    def transform(self, project, cxx_project, toolchain, **kwargs):
        for path in project.get_libpaths(toolchain, inherited=True):
            cxx_project.add_linkflag('{}{}'.format(self.prefix, path.path))


class PyBuildProjectLibPaths:
    MSVC = _PyBuildProjectLibPaths('/LIBPATH:')
    GNU = _PyBuildProjectLibPaths('-L')


class _PyBuildProjectDeps(Feature):
    def __init__(self, prefix):
        super(_PyBuildProjectDeps, self).__init__()
        self.prefix = prefix

    def transform(self, project, cxx_project, toolchain, **kwargs):
        for dep in project.get_dependencies(toolchain):
            if isinstance(dep.project, CXXLibrary):            
                libpath = os.path.join(toolchain.attributes.output, dep.project.name)
                cxx_project.add_linkflag('{}{}'.format(self.prefix, libpath))
                cxx_project.add_library(dep.project.name)            


class PyBuildProjectDeps:
    MSVC = _PyBuildProjectDeps("/LIBPATH:")
    GNU = _PyBuildProjectDeps("-L")


class PyBuildLinkLibrary(Feature):
    def __init__(self, libraries):
        super(PyBuildLinkLibrary, self).__init__()
        self.libraries = libraries if type(libraries) == list else [libraries]

    def transform(self, project, cxx_project, toolchain, **kwargs):
        for lib in self.libraries:
            cxx_project.add_dependency(lib)


class GNUFeatureFactory:
    def configure(self, toolchain):
        toolchain.add_feature(PyBuildCustomCFlag.C89, 'language-c89')
        toolchain.add_feature(PyBuildCustomCFlag.C99, 'language-c99')
        toolchain.add_feature(PyBuildCustomCFlag.C11, 'language-c11')
        toolchain.add_feature(PyBuildCustomCXXFlag.CXX11, 'language-c++11')
        toolchain.add_feature(PyBuildCustomCXXFlag.CXX14, 'language-c++14')
        toolchain.add_feature(PyBuildCustomCXXFlag.CXX17, 'language-c++17')
        toolchain.add_feature(PyBuildCustomCXXFlag('-g'), 'debug')
        toolchain.add_feature(PyBuildOptimize.GNU, 'optimize')
        toolchain.add_feature(PyBuildProjectMacros.GNU)
        toolchain.add_feature(PyBuildProjectIncPaths.GNU)
        toolchain.add_feature(PyBuildProjectLibPaths.GNU)
        toolchain.add_feature(PyBuildProjectDeps.GNU)
        toolchain.add_feature(PyBuildProjectLibraries.GNU)
