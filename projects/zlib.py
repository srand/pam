from build.model import CXXLibrary
from build.model import CXXExecutable

zlib = CXXLibrary('zlib')
zlib.add_sources('tests/zlib', r'.*\.c$')
zlib.add_macro('_CRT_SECURE_NO_WARNINGS', filter='windows-store')
zlib.add_macro('_CRT_NONSTDC_NO_WARNINGS', filter='windows-store')

zpipe = CXXExecutable('zpipe')
zpipe.add_sources('tests/zlib/examples/zpipe.c')
zpipe.add_incpath('tests/zlib')
zpipe.add_dependency(zlib)
zpipe.add_feature("zip", filter="msbuild")
