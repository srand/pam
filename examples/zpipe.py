from build.model import CXXLibrary
from build.model import CXXExecutable
from build.model import ToolchainGroup
from externals.zlib import zlib


toolchains = ToolchainGroup()
toolchains.add_toolchain('linux-x64-pam-gcc')
toolchains.add_toolchain('linux-x64-make-gcc')
toolchains.add_toolchain('windows-x64-msbuild-vs15')
toolchains.add_toolchain('windows-x64-pam-vs15')

zlib.add_toolchain_group(toolchains)

zpipe = CXXExecutable('zpipe')
zpipe.add_sources('output/zlib-source/', '.*zpipe.c', recurse=True)
zpipe.add_dependency(zlib)
zpipe.add_toolchain_group(toolchains)
