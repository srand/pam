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
from build.model import CXXLibrary, CXXExecutable
import os


class _MSBuildOptimize:
    def __init__(self):
        self.levels = {'disable': 'Disabled', 'space': 'MinSpace', 'speed': 'MaxSpeed', 'full': 'Full'}

    def transform(self, project, cxx_project, toolchain, **kwargs):
        if 'level' not in kwargs:
            raise ValueError('no "level" argument provided to optimize feature')
        if kwargs['level'] not in self.levels:
            raise ValueError('illegal "level" argument provided to optimize feature')
        value = self.levels[kwargs.get('level')]
        cxx_project.clcompile.optimize = value 


class MSBuildOptimize:
    MSVC = _MSBuildOptimize()


class MSBuildPlatformToolset:
    def __init__(self, toolset='v140', charset='MultiByte'):
        self.toolset = toolset
        self.charset = charset

    def transform(self, project, cxx_project, toolchain, **kwargs):
        cxx_project.config_props.toolset = self.toolset
        cxx_project.config_props.charset = self.charset


class _MSBuildProjectMacros(Feature):
    def __init__(self):
        super(_MSBuildProjectMacros, self).__init__()

    def transform(self, project, cxx_project, toolchain, **kwargs):
        for macro in project.get_macros(toolchain, inherited=True):
            cxx_project.add_macro(macro.key, macro.value)


class MSBuildProjectMacros:
    MSVC = _MSBuildProjectMacros()


class _MSBuildProjectIncPaths(Feature):
    def __init__(self):
        super(_MSBuildProjectIncPaths, self).__init__()

    def transform(self, project, cxx_project, toolchain, **kwargs):
        for path in project.get_incpaths(toolchain, inherited=True):
            cxx_project.add_incdir(path.path)


class MSBuildProjectIncPaths:
    MSVC = _MSBuildProjectIncPaths()


class _MSBuildProjectLibraries(Feature):
    def __init__(self):
        super(_MSBuildProjectLibraries, self).__init__()

    def transform(self, project, cxx_project, toolchain, **kwargs):
        for lib in project.get_libraries(toolchain, inherited=True):
            cxx_project.add_dependency(lib.name)


class MSBuildProjectLibraries:
    MSVC = _MSBuildProjectLibraries()


class _MSBuildProjectLibPaths(Feature):
    def __init__(self):
        super(_MSBuildProjectLibPaths, self).__init__()

    def transform(self, project, cxx_project, toolchain, **kwargs):
        for path in project.get_libpaths(toolchain, inherited=True):
            cxx_project.add_libdir(path.path)


class MSBuildProjectLibPaths:
    MSVC = _MSBuildProjectLibPaths()


class _MSBuildProjectDeps(Feature):
    def transform(self, project, cxx_project, toolchain, **kwargs):
        for dep in project.get_dependencies(toolchain):
            if isinstance(dep.project, CXXLibrary):
                cxx_project.add_libdir(
                    os.path.join(toolchain.attributes.output, dep.project.name))
                cxx_project.add_dependency('{lib}'.format(
                    output=toolchain.attributes.output, lib=dep.project.name))


class MSBuildProjectDeps:
    MSVC = _MSBuildProjectDeps()


class _MSBuildLinkLibrary(Feature):
    def __init__(self, libraries):
        super(_MSBuildLinkLibrary, self).__init__()
        self.libraries = libraries if type(libraries) == list else [libraries]

    def transform(self, project, cxx_project, toolchain, **kwargs):
        if isinstance(project, CXXExecutable):
            for lib in project.get_libraries(toolchain, inherited=True):
                cxx_project.add_dependency(lib.name)
            for lib in self.libraries:
                cxx_project.add_dependency(lib)


class MSBuildLinkLibrary(_MSBuildLinkLibrary):
    pass
