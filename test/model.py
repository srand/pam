import sys

import unittest
import shutil
import os
from build.transform.toolchain import ToolchainLoader, ToolchainRegistry
from build.model import CXXLibrary, CXXExecutable


class ModelTest(unittest.TestCase):
    def setUp(self):
        ToolchainLoader("toolchains").load()

    def tearDown(self):
        #if os.path.exists("output"):
        #    shutil.rmtree("output")
        pass
    
    def test_cxxproject_source(self):
        for toolchain in ToolchainRegistry.this_system():
            lib = CXXLibrary('test_cxxlib_source-{}'.format(toolchain.name))
            lib.add_sources('test/src/test_cxx_source.cpp')
            lib.add_sources('test/src', regex=r'.*source_regex\.cpp$')
            lib.add_sources('test/src', regex='.*never_matched.*')
            lib.add_sources('test/src/test_cxx_source_tool.unknown', tool='.cpp')
            lib.transform(toolchain)

            exe = CXXExecutable('test_cxxexe_source-{}'.format(toolchain.name))
            exe.add_sources('test/src/test_cxx_source_link.cpp')
            exe.add_dependency(lib)
            exe.transform(toolchain)

    def test_cxxproject_macro(self):
        for toolchain in ToolchainRegistry.this_system():
            lib = CXXLibrary('test_cxxlib_macro-{}'.format(toolchain.name))
            lib.add_macro('MACRO_PUBLISHED', publish=True)
            lib.add_macro('MACRO')
            lib.add_macro('UNMATCHED', filter='never-matched')
            lib.add_macro('MATCHED', filter='(windows|linux|mac)')
            lib.add_sources('test/src/test_cxx_macros.cpp')
            lib.transform(toolchain)

            exe = CXXExecutable('test_cxxexe_macro-{}'.format(toolchain.name))
            exe.add_sources('test/src/test_cxx_macros_link.cpp')
            exe.add_dependency(lib)
            exe.transform(toolchain)

    def test_cxxproject_incpath(self):
        for toolchain in ToolchainRegistry.this_system():
            lib = CXXLibrary('test_cxxlib_incpath-{}'.format(toolchain.name))
            lib.add_sources('test/src/test_cxx_incpath.cpp')
            lib.add_incpath('test/inc_private')
            lib.add_incpath('test/inc_public', publish=True)
            lib.add_incpath('test/inc_bad', filter='never_matched')
            lib.transform(toolchain)

            exe = CXXExecutable('test_cxxexe_incpath-{}'.format(toolchain.name))
            exe.add_sources('test/src/test_cxx_incpath_link.cpp')
            exe.add_dependency(lib)
            exe.transform(toolchain)

    def test_cxxproject_dependency(self):
        for toolchain in ToolchainRegistry.this_system():
            dep = CXXLibrary('test_cxxlib_dep_transitive-{}'.format(toolchain.name))
            dep.add_sources('test/src/test_cxx_dep_transitive.cpp')
            dep.transform(toolchain)

            lib = CXXLibrary('test_cxxlib_dep-{}'.format(toolchain.name))
            lib.add_sources('test/src/test_cxx_dep.cpp')
            lib.add_dependency(dep)
            lib.transform(toolchain)

            exe = CXXExecutable('test_cxxexe_dep-{}'.format(toolchain.name))
            exe.add_sources('test/src/test_cxx_dep_link.cpp')
            exe.add_dependency(lib)
            exe.transform(toolchain)
