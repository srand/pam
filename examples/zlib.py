from build.model import CXXLibrary
from build.model import CXXExecutable

zlib = CXXLibrary('zlib')
zlib.create_group('inflate').add_sources('tests/zlib', r'.*inflate.*\.c$')
zlib.create_group('deflate').add_sources('tests/zlib', r'.*deflate.*\.c$')
zlib.create_group('gz').add_sources('tests/zlib', r'.*gz.*\.c$')
zlib.add_macro('_CRT_SECURE_NO_WARNINGS', filter='windows-store')
zlib.add_macro('_CRT_NONSTDC_NO_WARNINGS', filter='windows-store')
zlib.add_macro('PAMBUILD', '1')

zpipe = CXXExecutable('zpipe')
zpipe.add_sources('tests/zlib/examples/zpipe.c')
zpipe.add_incpath('tests/zlib')
zpipe.add_dependency(zlib)
zpipe.add_feature("zip", filter="msbuild")
zpipe.add_toolchain('')
