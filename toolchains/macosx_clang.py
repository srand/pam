from build.transform.pybuild import CXXToolchain
from build.transform.toolchain import ToolchainExtender
from build.tools import clang
from build.features.pybuild import *
from build.requirement import HostRequirement



macosx = CXXToolchain("macosx-pam-clang")
macosx.add_tool('.S', clang.PyBuildCXXCompiler(cxx=False))
macosx.add_tool('.c', clang.PyBuildCXXCompiler(cxx=False))
macosx.add_tool('.cc', clang.PyBuildCXXCompiler(cxx=True))
macosx.add_tool('.cpp', clang.PyBuildCXXCompiler(cxx=True))
macosx.add_tool('.cxx', clang.PyBuildCXXCompiler(cxx=True))
macosx.archiver = clang.PyBuildCXXArchiver()
macosx.linker = clang.PyBuildCXXLinker()
macosx.add_requirement(HostRequirement.DARWIN)
macosx.add_feature(PyBuildCustomCFlag('-std=c89'), 'language-c89')
macosx.add_feature(PyBuildCustomCFlag('-std=c99'), 'language-c99')
macosx.add_feature(PyBuildCustomCFlag('-std=c11'), 'language-c11')
macosx.add_feature(PyBuildCustomCXXFlag('-std=c++11'), 'language-c++11')
macosx.add_feature(PyBuildCustomCXXFlag('-std=c++14'), 'language-c++14')
macosx.add_feature(PyBuildCustomCXXFlag('-std=c++17'), 'language-c++17')
macosx.add_feature(PyBuildOptimize(PyBuildOptimize.GNU), 'optimize')

macosx_x86 = ToolchainExtender("macosx-x86-pam-clang", macosx)
macosx_x86.add_feature(PyBuildCustomCFlag('-m32'))
macosx_x86.add_feature(PyBuildCustomCXXFlag('-m32'))
macosx_x86.add_feature(PyBuildCustomLinkerFlag('-m32'))

macosx_x64 = ToolchainExtender("macosx-x64-pam-clang", macosx)
macosx_x64.add_feature(PyBuildCustomCFlag('-m64'))
macosx_x64.add_feature(PyBuildCustomCXXFlag('-m64'))
macosx_x64.add_feature(PyBuildCustomLinkerFlag('-m64'))
