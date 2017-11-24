from build.model import *
from externals.ogg import ogg


version = "libvorbis-1.3.5"

source = URLPackage(
    "vorbis-source", 
    "http://downloads.xiph.org/releases/vorbis/{}.tar.gz".format(version))

def _source(*path):
    return os.path.join("output/vorbis-source", version, *path)

vorbis_srcs = [
    "mdct.c",
    "smallft.c",
    "block.c",
    "envelope.c",
    "window.c",
    "lsp.c",
    "lpc.c",
    "analysis.c",
    "synthesis.c",
    "psy.c",
    "info.c",
    "floor1.c",
    "floor0.c",
    "res0.c",
    "mapping0.c",
    "registry.c",
    "codebook.c",
    "sharedbook.c",
    "lookup.c",
    "bitrate.c",
]

vorbis = cxx_library(
    name = "vorbis",
    incpaths = [
        (_source("include"), {"publish": True}),
        _source("lib"),
    ],
    sources = [
        (_source("lib"), {"files": vorbis_srcs})
    ],
    dependencies = [source, ogg]
)
