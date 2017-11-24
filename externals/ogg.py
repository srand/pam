from build.model import *


version = "libogg-1.3.3"
source = URLPackage(
    "ogg-source", 
    "http://downloads.xiph.org/releases/ogg/{}.tar.gz".format(version))

def _source(*path):
    return os.path.join("output/ogg-source", version, *path)

ogg = cxx_library(
    name = "ogg",
    incpaths = [
        (_source("include"), {"publish": True}),
        (_source("."), {})
    ],
    commands = [
        {
            "output": _source("include", "ogg", "config_types.h"),
            "inputs": ["stdint.h"],
            "command": 'echo "#include <{inputs}>\ntypedef int16_t ogg_int16_t;\ntypedef uint16_t ogg_uint16_t;\ntypedef int32_t ogg_int32_t;\ntypedef uint32_t ogg_uint32_t;\ntypedef int64_t ogg_int64_t;" > {output}'
        }
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
