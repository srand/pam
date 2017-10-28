from build.model import CXXLibrary
from build.model import CXXExecutable

zlib = CXXLibrary('zlib')
zlib.add_sources('zlib', r'.*\.c$')
zlib.add_macro('_CRT_SECURE_NO_WARNINGS', filter='windows-store')
zlib.add_macro('_CRT_NONSTDC_NO_WARNINGS', filter='windows-store')
zlib.add_toolchain('linux-x64-pam-gcc')
zlib.add_toolchain('linux-x64-make-gcc')

zpipe = CXXExecutable('zpipe')
zpipe.add_sources('zlib/examples/zpipe.c')
zpipe.add_incpath('zlib')
zpipe.add_dependency(zlib)
zpipe.add_toolchain('linux-x64-pam-gcc')
zpipe.add_toolchain('linux-x64-make-gcc')
