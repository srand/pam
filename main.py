from project import CXXLibrary
from project import CXXExecutable
from transform.msbuild import MSBuildCXXToolchain
from transform.native import MSVCCXXToolchain
from transform.native import VS2015Environment

toolchain = MSVCCXXToolchain('win-x86-vs2013xp', VS2015Environment())
#toolchain = MSBuildCXXToolchain('Debug', 'Win32', 'v120_xp', 'win-x86-vs2013xp')

zlib = CXXLibrary('zlib')
zlib.add_sources('tests/zlib', r'.*\.c$')
zlib.transform(toolchain)

zpipe = CXXExecutable('zpipe')
zpipe.add_sources('tests/zlib/examples/zpipe.c')
zpipe.add_incpath('tests/zlib')
zpipe.add_dependency(zlib)
zpipe.transform(toolchain)
