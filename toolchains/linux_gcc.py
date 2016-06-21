from build.transform.pybuild import CXXToolchain
from build.tools.gnu import PyBuildCXXCompiler, PyBuildCXXArchiver, PyBuildCXXLinker
from build.features.gnu import PyBuildWordsize

linux_x86 = CXXToolchain("linux-x86-pybuild-gcc")
linux_x86.add_tool('.S', PyBuildCXXCompiler(cxx=False))
linux_x86.add_tool('.c', PyBuildCXXCompiler(cxx=False))
linux_x86.add_tool('.cc', PyBuildCXXCompiler(cxx=True))
linux_x86.add_tool('.cpp', PyBuildCXXCompiler(cxx=True))
linux_x86.add_tool('.cxx', PyBuildCXXCompiler(cxx=True))
linux_x86.archiver = PyBuildCXXArchiver()
linux_x86.linker = PyBuildCXXLinker()
linux_x86.add_feature(PyBuildWordsize(32))

linux_x64 = CXXToolchain("linux-x64-pybuild-gcc")
linux_x64.add_tool('.S', PyBuildCXXCompiler(cxx=False))
linux_x64.add_tool('.c', PyBuildCXXCompiler(cxx=False))
linux_x64.add_tool('.cc', PyBuildCXXCompiler(cxx=True))
linux_x64.add_tool('.cpp', PyBuildCXXCompiler(cxx=True))
linux_x64.add_tool('.cxx', PyBuildCXXCompiler(cxx=True))
linux_x64.archiver = PyBuildCXXArchiver()
linux_x64.linker = PyBuildCXXLinker()
linux_x86.add_feature(PyBuildWordsize(64))
