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
gcc.add_feature(PyBuildCustomCFlag('-std=c89'), 'language-c89')
gcc.add_feature(PyBuildCustomCFlag('-std=c99'), 'language-c99')
gcc.add_feature(PyBuildCustomCFlag('-std=c11'), 'language-c11')
gcc.add_feature(PyBuildCustomCXXFlag('-std=c++11'), 'language-c++11')
gcc.add_feature(PyBuildCustomCXXFlag('-std=c++14'), 'language-c++14')
gcc.add_feature(PyBuildCustomCXXFlag('-std=c++17'), 'language-c++17')
gcc.add_feature(PyBuildOptimize(PyBuildOptimize.GNU), 'optimize')
gcc.add_feature(PyBuildCustomCXXFlag('-g'), 'debug')

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
