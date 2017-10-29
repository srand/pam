from build.model import CXXLibrary
from build.model import CXXExecutable
from externals.zlib import zlib as zlib_ext

zlib = CXXLibrary('zlib')
zlib.add_sources('zlib', r'.*\.c$')
zlib.add_toolchain('linux-x64-pam-gcc')
zlib.add_toolchain('linux-x64-make-gcc')
zlib.add_incpath("zlib", publish=True)

zpipe = CXXExecutable('zpipe')
zpipe.add_sources('zlib/examples/zpipe.c')
zpipe.add_dependency(zlib_ext)
zpipe.add_toolchain('linux-x64-pam-gcc')
zpipe.add_toolchain('linux-x64-make-gcc')
zpipe.add_toolchain('windows-x64-msbuild-vs15')
zpipe.add_toolchain('windows-x64-pam-vs15')
