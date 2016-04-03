from project import CXXLibrary
from project import CXXExecutable
from transform.msbuild import MSBuildCXXToolchain
from transform.native import MSVCCXXToolchain
from transform.native import VS2015Environment

#toolchain = MSVCCXXToolchain(VS2015Environment())
toolchain = MSBuildCXXToolchain('Debug', 'Win32', 'v120_xp')

lib = CXXLibrary('zlib')
lib.add_sources('tests/zlib', r'.*\.c$')
lib.transform(toolchain)

example = CXXExecutable('zpipe')
example.add_sources('tests/zlib/examples/zpipe.c')
example.add_incpath('tests/zlib')
example.add_dependency(lib)
example.transform(toolchain)