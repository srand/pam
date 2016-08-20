from build.model import CXXLibrary
from build.model import CXXExecutable
from build.model import ToolchainGroup 

toolchains = ToolchainGroup()
toolchains.add_toolchain('windows-x86-msbuild-vs14')
toolchains.add_toolchain('windows-x64-msbuild-vs14')
toolchains.add_toolchain('windows-x86-pybuild-vs14')
toolchains.add_toolchain('windows-x64-pybuild-vs14')

zlib = CXXLibrary('zlib')
zlib.add_sources('tests/zlib', r'.*\.c$')
zlib.add_macro('_CRT_SECURE_NO_WARNINGS', filter='windows-store')
zlib.add_macro('_CRT_NONSTDC_NO_WARNINGS', filter='windows-store')
zlib.add_toolchain_group(toolchains)

zpipe = CXXExecutable('zpipe')
zpipe.add_sources('tests/zlib/examples/zpipe.c')
zpipe.add_incpath('tests/zlib')
zpipe.add_dependency(zlib)
zpipe.add_feature("zip", filter="msbuild")
zpipe.add_toolchain_group(toolchains)
