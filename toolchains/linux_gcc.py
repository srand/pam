from build.transform.pybuild import CXXToolchain
from build.tools import gnu

linux_x86 = CXXToolchain("linux-x86-pybuild-gcc")
linux_x86.add_tool('.S', gnu.PyBuildCXXCompiler(cxx=False))
linux_x86.add_tool('.c', gnu.PyBuildCXXCompiler(cxx=False))
linux_x86.add_tool('.cc', gnu.PyBuildCXXCompiler(cxx=True))
linux_x86.add_tool('.cpp', gnu.PyBuildCXXCompiler(cxx=True))
linux_x86.add_tool('.cxx', gnu.PyBuildCXXCompiler(cxx=True))
linux_x86.archiver = gnu.PyBuildCXXArchiver()
linux_x86.linker = gnu.PyBuildCXXLinker()
linux_x86.add_cflag('-m32')
linux_x86.add_cxxflag('-m32')
linux_x86.add_linkflag('-m32')

linux_x64 = CXXToolchain("linux-x64-pybuild-gcc")
linux_x64.add_tool('.S', gnu.PyBuildCXXCompiler(cxx=False))
linux_x64.add_tool('.c', gnu.PyBuildCXXCompiler(cxx=False))
linux_x64.add_tool('.cc', gnu.PyBuildCXXCompiler(cxx=True))
linux_x64.add_tool('.cpp', gnu.PyBuildCXXCompiler(cxx=True))
linux_x64.add_tool('.cxx', gnu.PyBuildCXXCompiler(cxx=True))
linux_x64.archiver = gnu.PyBuildCXXArchiver()
linux_x64.linker = gnu.PyBuildCXXLinker()
linux_x64.add_cflag('-m64')
linux_x64.add_cxxflag('-m64')
linux_x64.add_linkflag('-m64')

