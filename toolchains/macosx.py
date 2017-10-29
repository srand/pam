from build.transform import xcbuild
from build.transform.toolchain import ToolchainExtender
from build.tools import clang
from build.features.pybuild import *
from build.requirement import HostRequirement


xcbuild = xcbuild.CXXToolchain("xcbuild-clang")
xcbuild.add_tool('.c', clang.XcBuildCXXCompiler('c'))
xcbuild.add_tool('.cc', clang.XcBuildCXXCompiler('c++'))
xcbuild.add_tool('.cpp', clang.XcBuildCXXCompiler('c++'))
xcbuild.add_tool('.cxx', clang.XcBuildCXXCompiler('c++'))
xcbuild.add_requirement(HostRequirement.DARWIN)
#xcbuild.add_feature(PyBuildCustomCFlag('-std=c89'), 'language-c89')
#cbuild.add_feature(PyBuildCustomCFlag('-std=c99'), 'language-c99')
#xcbuild.add_feature(PyBuildCustomCFlag('-std=c11'), 'language-c11')
#xcbuild.add_feature(PyBuildCustomCXXFlag('-std=c++11'), 'language-c++11')
#xcbuild.add_feature(PyBuildCustomCXXFlag('-std=c++14'), 'language-c++14')
#xcbuild.add_feature(PyBuildCustomCXXFlag('-std=c++17'), 'language-c++17')
#xcbuild.add_feature(PyBuildOptimize(PyBuildOptimize.GNU), 'optimize')

macosx_x86 = ToolchainExtender("macosx-x86-xcbuild-clang", xcbuild)
#macosx_x86.add_feature(PyBuildCustomCFlag('-m32'))
#macosx_x86.add_feature(PyBuildCustomCXXFlag('-m32'))
#macosx_x86.add_feature(PyBuildCustomLinkerFlag('-m32'))

macosx_x64 = ToolchainExtender("macosx-x64-xcbuild-clang", xcbuild)
#macosx_x64.add_feature(PyBuildCustomCFlag('-m64'))
#macosx_x64.add_feature(PyBuildCustomCXXFlag('-m64'))
#macosx_x64.add_feature(PyBuildCustomLinkerFlag('-m64'))
