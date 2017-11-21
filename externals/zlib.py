from build.model import URLPackage, cxx_library

version = "1.2.11"

source = URLPackage("zlib-source", "https://zlib.net/zlib-{}.tar.gz".format(version))

zlib = cxx_library(
    'zlib',
    sources=[
        ('output/zlib-source/zlib-{}'.format(version), {"regex": '.*\.c$'})
    ],
    incpaths=[
        ('output/zlib-source/zlib-{}'.format(version), {"publish": True})
    ],
    features=[
        "language-c89"
    ],
    dependencies=[
        source
    ]
)
