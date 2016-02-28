from transform import Library
from transform import Executable
from transform import GNUCompilerDriver
from transform import mac_x86_libcxx_settings
from transform import ios_x86_libcxx_settings
from transform import ios_armv7_libcxx_settings
from transform import win_x86_vs2015xp_settings

settings = win_x86_vs2015xp_settings()
settings.add_define('FOOBAR')

lib = Library('zlib', settings)
lib.add_sources('tests/zlib', r'.*\.c$')
lib.transform()

example = Executable('tests/zlib/zpipe', settings)
example.add_sources('tests/zlib/examples/zpipe.c')
example.add_incpath('tests/zlib')
example.add_library(lib)
example.transform()
