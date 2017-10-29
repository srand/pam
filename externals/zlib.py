from build.model import URLPackage, CXXLibrary

version = "1.2.11"

source = URLPackage("zlib-source", "https://zlib.net/zlib-{}.tar.gz".format(version))

zlib = CXXLibrary('zlib')
zlib.add_incpath('output/zlib-source/zlib-{}'.format(version), publish=True)
zlib.add_sources('output/zlib-source/zlib-{}'.format(version), r'.*\.c$')
zlib.add_dependency(source)
