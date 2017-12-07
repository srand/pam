from build.model import *
from externals.freetype import freetype
from externals.vorbis import vorbis
import os


version = "SDL2-2.0.7"
source = URLPackage("SDL2-source", "https://www.libsdl.org/release/{}.zip".format(version))

def _source(path):
    return os.path.join("output", "SDL2-source", version, path)

sdl2 = cxx_library(
    name = "SDL2",
    incpaths = [
        (_source("include"), {"publish": True})
    ],
    sources = [
        (_source("src"), {"regex": ".*\.c$"}),
        (_source("src/atomic"), {"regex": ".*\.c$"}),
        (_source("src/audio"), {"regex": ".*\.c$"}),
        (_source("src/audio/dummy"), {"regex": ".*\.c$"}),
        (_source("src/cpuinfo"), {"regex": ".*\.c$"}),
        (_source("src/dynapi"), {"regex": ".*\.c$"}),
        (_source("src/events"), {"regex": ".*\.c$"}),
        (_source("src/file"), {"regex": ".*\.c$"}),
        (_source("src/haptic"), {"regex": ".*\.c$"}),
        (_source("src/joystick"), {"regex": ".*\.c$"}),
        (_source("src/libm"), {"regex": ".*\.c$"}),
        (_source("src/power"), {"regex": ".*\.c$"}),
        (_source("src/render"), {"regex": ".*\.c$", "recurse": True}),
        (_source("src/stdlib"), {"regex": ".*\.c$"}),
        (_source("src/thread"), {"regex": ".*\.c$"}),
        (_source("src/timer"), {"regex": ".*\.c$"}),
        (_source("src/video"), {"regex": ".*\.c$"}),
        (_source("src/video/dummy"), {"regex": ".*\.c$"}),

        (_source("src/core/linux"), {"regex": ".*\.c$", "filter": "linux"}),
        (_source("src/joystick/linux"), {"regex": ".*\.c$", "filter": "linux"}),
        (_source("src/joystick/steam"), {"regex": ".*\.c$", "filter": "linux"}),
        (_source("src/power/linux"), {"regex": ".*\.c$", "filter": "linux"}),
        (_source("src/filesystem/unix"), {"regex": ".*\.c$", "filter": "linux"}),
        (_source("src/timer/unix"), {"regex": ".*\.c$", "filter": "linux"}),

        (_source("src/audio/wasapi"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/audio/directsound"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/audio/disk"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/audio/winmm"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/core/windows"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/filesystem/windows"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/haptic/windows"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/joystick/windows"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/joystick/steam"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/loadso/windows"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/power/windows"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/thread/windows/SDL_sysmutex.c"), {"filter": "windows"}),
        (_source("src/thread/windows/SDL_syssem.c"), {"filter": "windows"}),
        (_source("src/thread/windows/SDL_systhread.c"), {"filter": "windows"}),
        (_source("src/thread/windows/SDL_systls.c"), {"filter": "windows"}),
        (_source("src/thread/generic/SDL_syscond.c"), {"filter": "windows"}),
        (_source("src/timer/windows"), {"regex": ".*\.c$", "filter": "windows"}),
        (_source("src/video/windows"), {"regex": ".*\.c$", "filter": "windows"}),
    ],
    libraries = [
        ("version", {"filter": "windows", "publish": True})
    ],
    dependencies = [source]
)

sdl2_main = cxx_library(
    name = "SDL2main",
    incpaths = [
        (_source("include"), {"publish": True})
    ],
    sources = [
        (_source("src/main/dummy"), {"regex": ".*\.c$", "filter": "linux"}),
        (_source("src/main/windows"), {"regex": ".*\.c$", "filter": "windows"}),
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
    macros = [
        ("WIN32", {"filter": "windows"})
    ],
    sources = [
	_source("SDLnet.c"),
	_source("SDLnetTCP.c"),
	_source("SDLnetUDP.c"),
	_source("SDLnetselect.c"),
    ],
    libraries = [
        ("iphlpapi", {"filter": "windows", "publish": True}),
        ("ws2_32", {"filter": "windows", "publish": True}),
        ("winmm", {"filter": "windows", "publish": True}),
        ("imm32", {"filter": "windows", "publish": True}),
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
        (_source("."), {"publish": True})
    ],
    sources = [
        _source("SDL_ttf.c")
    ],
    dependencies = [source_ttf, sdl2, freetype]
)

#####################################################################################

version_mixer = "SDL2_mixer-2.0.2"

source_mixer = URLPackage("SDL2_mixer-source", "https://www.libsdl.org/projects/SDL_mixer/release/{}.zip".format(version_mixer))

def _source(path):
    return os.path.join("output", "SDL2_mixer-source", version_mixer, path)

sdl2_mixer = cxx_library(
    name = "SDL2_mixer",
    incpaths = [
        (_source("."), {"publish": True})
    ],
    macros = [
        "MUSIC_WAV",
        "MUSIC_OGG",
    ],
    sources = [
        (_source("."), {"regex": ".*\.c$"})
    ],
    dependencies = [source_mixer, sdl2, freetype, vorbis]
)

#####################################################################################
