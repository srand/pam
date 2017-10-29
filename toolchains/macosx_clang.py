from build.transform.pybuild import CXXToolchain
from build.transform.toolchain import ToolchainExtender
from build.tools import clang
from build.features.pybuild import *
from build.requirement import HostRequirement


macosx = CXXToolchain("macosx-pam-clang")
macosx.add_tool('.s', clang.PyBuildCXXCompiler('assembler'))
macosx.add_tool('.S', clang.PyBuildCXXCompiler('assembler-with-cpp'))
macosx.add_tool('.c', clang.PyBuildCXXCompiler('c'))
macosx.add_tool('.cc', clang.PyBuildCXXCompiler('c++'))
macosx.add_tool('.cpp', clang.PyBuildCXXCompiler('c++'))
macosx.add_tool('.cxx', clang.PyBuildCXXCompiler('c++'))
macosx.archiver = clang.PyBuildCXXArchiver()
macosx.linker = clang.PyBuildCXXLinker()
macosx.add_requirement(HostRequirement.DARWIN)
macosx.add_feature(PyBuildCustomCFlag.C89, 'language-c89')
macosx.add_feature(PyBuildCustomCFlag.C99, 'language-c99')
macosx.add_feature(PyBuildCustomCFlag.C11, 'language-c11')
macosx.add_feature(PyBuildCustomCXXFlag.CXX11, 'language-c++11')
macosx.add_feature(PyBuildCustomCXXFlag.CXX14, 'language-c++14')
macosx.add_feature(PyBuildCustomCXXFlag.CXX17, 'language-c++17')
macosx.add_feature(PyBuildOptimize.GNU, 'optimize')
macosx.add_feature(PyBuildProjectMacros.GNU)
macosx.add_feature(PyBuildProjectIncPaths.GNU)
macosx.add_feature(PyBuildProjectLibPaths.GNU)
macosx.add_feature(PyBuildProjectDeps.ALL)

macosx_x86 = ToolchainExtender("macosx-x86-pam-clang", macosx)
macosx_x86.add_feature(PyBuildCustomCFlag('-m32'))
macosx_x86.add_feature(PyBuildCustomCXXFlag('-m32'))
macosx_x86.add_feature(PyBuildCustomLinkerFlag('-m32'))

macosx_x64 = ToolchainExtender("macosx-x64-pam-clang", macosx)
macosx_x64.add_feature(PyBuildCustomCFlag('-m64'))
macosx_x64.add_feature(PyBuildCustomCXXFlag('-m64'))
macosx_x64.add_feature(PyBuildCustomLinkerFlag('-m64'))
