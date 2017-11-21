from build.model import *
from toolchains.pam import *
from externals.zlib import zlib


pam_gnu_toolchain(
    "linux-x64-pam-gcc",
    inherits="linux-pam-gcc",
    cflags="-m64",
    cxxflags="-m64",
    linkflags="-m64"
)

pam_gnu_toolchain(
    "linux-arm-pam-gcc",
    prefix="arm-linux-gnueabi-"
)

pam_msvc_toolchain(
    "windows-x64-pam-vs15-rtti",
    inherits='windows-x64-pam-vs15',
    cxxflags="/rtti",
)

toolchains = [
    'linux-x64-pam-gcc',
    'linux-arm-pam-gcc',
    'linux-make-gcc',
    'windows-x64-msbuild-vs15',
    'windows-x64-pam-vs15'
]

map(zlib.add_toolchain, toolchains)

zpipe = cxx_executable(
    'zpipe',
    sources=[
        ('output/zlib-source/', {"regex": '.*zpipe.c', "recurse": True})
    ],
    dependencies=[zlib],
    toolchains=toolchains
)
