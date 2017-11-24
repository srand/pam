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
        (_source("."), {"files": [
            "src/autofit/autofit.c",
            "src/bdf/bdf.c",
            "src/cff/cff.c",
            "src/base/ftbase.c",
            "src/base/ftbbox.c",
            "src/base/ftbitmap.c",
            "src/base/ftfstype.c",
            "src/base/ftfntfmt.c",
            "src/base/ftgasp.c",
            "src/base/ftglyph.c",
            "src/base/ftinit.c",
            "src/base/ftmm.c",
            "src/base/ftpfr.c",
            "src/base/ftsynth.c",
            "src/base/fttype1.c",
            "src/base/ftwinfnt.c",
            "src/base/ftlcdfil.c",
            "src/base/ftgxval.c",
            "src/base/ftotval.c",
            "src/base/ftpatent.c",
            "src/base/ftstroke.c",
            "src/base/ftsystem.c",
            "src/cache/ftcache.c",
            "src/gzip/ftgzip.c",
            "src/lzw/ftlzw.c",
            "src/smooth/smooth.c",
            "src/pcf/pcf.c",
            "src/pfr/pfr.c",
            "src/psaux/psaux.c",
            "src/pshinter/pshinter.c",
            "src/psnames/psmodule.c",
            "src/raster/raster.c",
            "src/sfnt/sfnt.c",
            "src/truetype/truetype.c",
            "src/type1/type1.c",
            "src/cid/type1cid.c",
            "src/type42/type42.c",
            "src/winfonts/winfnt.c",
        ]})
    ],
    dependencies = [source]
)
