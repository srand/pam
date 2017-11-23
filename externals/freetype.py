from build.model import *
import os


version = "2.8.1"
source = URLPackage("freetype-source", "https://download.savannah.gnu.org/releases/freetype/ft{}.zip".format(version.replace(".","")))

def _source(path):
    return os.path.join("output", "freetype-source", "freetype-{}".format(version), path)

freetype = cxx_library(
    name = "freetype",
    incpaths = [
        (_source("include"), {"publish": True})
    ],
    macros = [
        "FT2_BUILD_LIBRARY"
    ],
    sources = [
        (_source("src/base"), {"regex": ".*\.c$"}),
        (_source("src/truetype"), {"regex": ".*\.c$"})
    ],
    dependencies = [source]
)
