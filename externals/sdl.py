from build.model import *
import os


version = "SDL2-2.0.7"
source = URLPackage("sdl2-source", "https://www.libsdl.org/release/{}.zip".format(version))

def _source(path):
    return os.path.join("output", "sdl2-source", version, path)

sdl2 = cxx_library(
    name = "SDL2",
    incpaths = [
        (_source("include"), {"publish": True})
    ],
    commands = [
        #output = _source("include"),
    ],
    sources = [
        (_source("src"), {"regex": ".*\.c$"}),
        (_source("src/atomic"), {"regex": ".*\.c$"}),
        (_source("src/audio"), {"regex": ".*\.c$"}),
        (_source("src/cpuinfo"), {"regex": ".*\.c$"}),
        (_source("src/dynapi"), {"regex": ".*\.c$"}),
        (_source("src/events"), {"regex": ".*\.c$"}),
        (_source("src/file"), {"regex": ".*\.c$"}),
        (_source("src/libm"), {"regex": ".*\.c$"}),
        (_source("src/render"), {"regex": ".*\.c$", "recurse": True}),
        (_source("src/stdlib"), {"regex": ".*\.c$"}),
        (_source("src/thread"), {"regex": ".*\.c$"}),
        (_source("src/timer"), {"regex": ".*\.c$"}),
        (_source("src/video"), {"regex": ".*\.c$"}),

        (_source("src/core/linux"), {"regex": ".*\.c$", "filter": "linux"}),
        (_source("src/joystick/linux"), {"regex": ".*\.c$", "filter": "linux"}),
        (_source("src/joystick/steam"), {"regex": ".*\.c$", "filter": "linux"}),
        (_source("src/power/linux"), {"regex": ".*\.c$", "filter": "linux"}),
        (_source("src/filesystem/unix"), {"regex": ".*\.c$", "filter": "linux"}),
        (_source("src/timer/unix"), {"regex": ".*\.c$", "filter": "linux"}),
    ],
)

sdl2_main = cxx_library(
    name = "SDL2main",
    incpaths = [
        (_source("include"), {"publish": True})
    ],
    sources = [
        (_source("src/main/dummy"), {"regex": ".*\.c$", "filter": "linux"}),
    ]
)

#####################################################################################

version_net = "SDL2_net-2.0.1"

source_net = URLPackage("SDL2_net-source", "https://www.libsdl.org/projects/SDL_net/release/{}.zip".format(version_net))

def _source(path):
    return os.path.join("output", "SDL2_net-source", version_net, path)

sdl2_net = cxx_library(
    name = "SDL2_net",
    incpaths = [
        (_source("."), {"publish": True})
    ],
    sources = [
	_source("SDLnet.c"),
	_source("SDLnetTCP.c"),
	_source("SDLnetUDP.c"),
	_source("SDLnetselect.c"),
    ],
    dependencies = [source_net, sdl2]
)

#####################################################################################

version_image = "SDL2_image-2.0.2"

source_image = URLPackage("SDL2_image-source", "https://www.libsdl.org/projects/SDL_image/release/{}.zip".format(version_image))

def _source(path):
    return os.path.join("output", "SDL2_image-source", version_image, path)

sdl2_image = cxx_library(
    name = "SDL2_image",
    incpaths = [
        (_source("."), {"publish": True})
    ],
    sources = [
	_source("IMG.c"),
	_source("IMG_bmp.c"),
	_source("IMG_gif.c"),
	_source("IMG_jpg.c"),
	_source("IMG_lbm.c"),
	_source("IMG_pcx.c"),
	_source("IMG_png.c"),
	_source("IMG_pnm.c"),
	_source("IMG_svg.c"),
	_source("IMG_tga.c"),
	_source("IMG_tif.c"),
	_source("IMG_xcf.c"),
	_source("IMG_xpm.c"),
	_source("IMG_xv.c"),
	_source("IMG_webp.c"),
    ],
    dependencies = [source_image, sdl2]
)

#####################################################################################

version_ttf = "SDL2_ttf-2.0.14"

source_ttf = URLPackage("SDL2_ttf-source", "https://www.libsdl.org/projects/SDL_ttf/release/{}.zip".format(version_ttf))

def _source(path):
    return os.path.join("output", "SDL2_ttf-source", version_ttf, path)

sdl2_ttf = cxx_library(
    name = "SDL2_ttf",
    incpaths = [
        "/usr/include/freetype2",
        (_source("."), {"publish": True})
    ],
    sources = [
        _source("SDL_ttf.c")
    ],
    dependencies = [source_ttf, sdl2]
)

#####################################################################################
