from build.transform.pybuild import CXXToolchain
from build.transform.toolchain import ToolchainExtender
from build.tools.gnu import PyBuildCXXCompiler, PyBuildCXXArchiver, PyBuildCXXLinker
from build.features.pybuild import *
from build.requirement import HostRequirement 


gcc = CXXToolchain("pam-gcc")
gcc.add_tool('.S', PyBuildCXXCompiler(cxx=False))
gcc.add_tool('.c', PyBuildCXXCompiler(cxx=False))
gcc.add_tool('.cc', PyBuildCXXCompiler(cxx=True))
gcc.add_tool('.cpp', PyBuildCXXCompiler(cxx=True))
gcc.add_tool('.cxx', PyBuildCXXCompiler(cxx=True))
gcc.archiver = PyBuildCXXArchiver()
gcc.linker = PyBuildCXXLinker()
gcc.add_feature(PyBuildCustomCXXFlag('-std=c++11'), 'c++11')
gcc.add_feature(PyBuildCustomCXXFlag('-std=c++14'), 'c++14')
gcc.add_feature(PyBuildCustomCXXFlag('-std=c++17'), 'c++17')

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
