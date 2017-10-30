from build.transform.pybuild import CXXToolchain as PamCXXToolchain
from build.transform.make import CXXToolchain as MakeCXXToolchain
from build.transform.toolchain import ToolchainExtender
from build.tools.gnu import PyBuildCXXCompiler, PyBuildCXXArchiver, PyBuildCXXLinker
from build.features.pybuild import *
from build.requirement import HostRequirement 


gcc = PamCXXToolchain("pam-gcc")
gcc.add_tool('.s', PyBuildCXXCompiler('assembler'))
gcc.add_tool('.S', PyBuildCXXCompiler('assembler-with-cpp'))
gcc.add_tool('.c', PyBuildCXXCompiler('c'))
gcc.add_tool('.cc', PyBuildCXXCompiler('c++'))
gcc.add_tool('.cpp', PyBuildCXXCompiler('c++'))
gcc.add_tool('.cxx', PyBuildCXXCompiler('c++'))
gcc.archiver = PyBuildCXXArchiver()
gcc.linker = PyBuildCXXLinker()
gcc.add_feature(PyBuildCustomCFlag.C89, 'language-c89')
gcc.add_feature(PyBuildCustomCFlag.C99, 'language-c99')
gcc.add_feature(PyBuildCustomCFlag.C11, 'language-c11')
gcc.add_feature(PyBuildCustomCXXFlag.CXX11, 'language-c++11')
gcc.add_feature(PyBuildCustomCXXFlag.CXX14, 'language-c++14')
gcc.add_feature(PyBuildCustomCXXFlag.CXX17, 'language-c++17')
gcc.add_feature(PyBuildCustomCXXFlag('-g'), 'debug')
gcc.add_feature(PyBuildOptimize.GNU, 'optimize')
gcc.add_feature(PyBuildProjectMacros.GNU)
gcc.add_feature(PyBuildProjectIncPaths.GNU)
gcc.add_feature(PyBuildProjectLibPaths.GNU)
gcc.add_feature(PyBuildProjectDeps.GNU)
gcc.add_feature(PyBuildProjectLibraries.GNU)

linux = ToolchainExtender("linux-pam-gcc", gcc)
linux.add_requirement(HostRequirement.LINUX)

linux_x86 = ToolchainExtender("linux-x86-pam-gcc", linux)
linux_x86.add_feature(PyBuildCustomCFlag('-m32'))
linux_x86.add_feature(PyBuildCustomCXXFlag('-m32'))
linux_x86.add_feature(PyBuildCustomLinkerFlag('-m32'))

linux_x64 = ToolchainExtender("linux-x64-pam-gcc", linux)
linux_x86.add_feature(PyBuildCustomCFlag('-m64'))
linux_x86.add_feature(PyBuildCustomCXXFlag('-m64'))
linux_x86.add_feature(PyBuildCustomLinkerFlag('-m64'))

linux_arm = ToolchainExtender("linux-arm-pam-gcc", linux)


gcc_mk = MakeCXXToolchain("make-gcc")
gcc_mk.add_tool('.s', PyBuildCXXCompiler('assembler'))
gcc_mk.add_tool('.S', PyBuildCXXCompiler('assembler-with-cpp'))
gcc_mk.add_tool('.c', PyBuildCXXCompiler('c'))
gcc_mk.add_tool('.cc', PyBuildCXXCompiler('c++'))
gcc_mk.add_tool('.cpp', PyBuildCXXCompiler('c++'))
gcc_mk.add_tool('.cxx', PyBuildCXXCompiler('c++'))
gcc_mk.archiver = PyBuildCXXArchiver()
gcc_mk.linker = PyBuildCXXLinker()
gcc_mk.add_feature(PyBuildCustomCFlag.C89, 'language-c89')
gcc_mk.add_feature(PyBuildCustomCFlag.C99, 'language-c99')
gcc_mk.add_feature(PyBuildCustomCFlag.C11, 'language-c11')
gcc_mk.add_feature(PyBuildCustomCXXFlag.CXX11, 'language-c++11')
gcc_mk.add_feature(PyBuildCustomCXXFlag.CXX14, 'language-c++14')
gcc_mk.add_feature(PyBuildCustomCXXFlag.CXX17, 'language-c++17')
gcc_mk.add_feature(PyBuildCustomCXXFlag('-g'), 'debug')
gcc_mk.add_feature(PyBuildOptimize.GNU, 'optimize')
gcc_mk.add_feature(PyBuildProjectMacros.GNU)
gcc_mk.add_feature(PyBuildProjectIncPaths.GNU)
gcc_mk.add_feature(PyBuildProjectLibPaths.GNU)
gcc_mk.add_feature(PyBuildProjectDeps.GNU)
gcc_mk.add_feature(PyBuildProjectLibraries.GNU)

linux_mk = ToolchainExtender("linux-make-gcc", gcc_mk)
linux_mk.add_requirement(HostRequirement.LINUX)

linux_x86_mk = ToolchainExtender("linux-x86-make-gcc", linux_mk)
linux_x86_mk.add_feature(PyBuildCustomCFlag('-m32'))
linux_x86_mk.add_feature(PyBuildCustomCXXFlag('-m32'))
linux_x86_mk.add_feature(PyBuildCustomLinkerFlag('-m32'))

linux_x64_mk = ToolchainExtender("linux-x64-make-gcc", linux_mk)
linux_x86_mk.add_feature(PyBuildCustomCFlag('-m64'))
linux_x86_mk.add_feature(PyBuildCustomCXXFlag('-m64'))
linux_x86_mk.add_feature(PyBuildCustomLinkerFlag('-m64'))
