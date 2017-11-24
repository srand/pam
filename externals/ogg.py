from build.model import *


version = "libogg-1.3.3"


def _source(*path):
    return os.path.join("output/ogg-source", version, *path)

class PatchedURLPackage(URLPackage):
    def __init__(self, *args, **kwargs):
        super(PatchedURLPackage, self).__init__(*args, **kwargs)

    def transform(self, *args, **kwargs):
        super(PatchedURLPackage, self).transform(*args, **kwargs)

        with open(_source("include", "ogg", "config_types.h"), "w") as f:
            f.write("""
#ifndef CONFIG_TYPES_H
#define CONFIG_TYPES_H
#include <stdint.h>
typedef int16_t ogg_int16_t;
typedef uint16_t ogg_uint16_t;
typedef int32_t ogg_int32_t;
typedef uint32_t ogg_uint32_t;
typedef int64_t ogg_int64_t;
#endif // CONFIG_TYPES_H
""")

source = PatchedURLPackage(
    "ogg-source", 
    "http://downloads.xiph.org/releases/ogg/{}.tar.gz".format(version))


ogg = cxx_library(
    name = "ogg",
    incpaths = [
        (_source("include"), {"publish": True}),
        (_source("."), {})
    ],
    macros = [
        ("ogg_int16_t", {"value": "int16_t"}),
        ("ogg_uint16_t", {"value": "uint16_t"}),
        ("ogg_int32_t", {"value": "int32_t"}),
        ("ogg_uint32_t", {"value": "uint32_t"}),
        ("ogg_int64_t", {"value": "int64_t"}),
        ("ogg_uint64_t", {"value": "uint64_t"}),
    ],
    sources = [
        (_source("src"), {"regex": ".*\.c$"})
    ],
    dependencies = [source]
)
