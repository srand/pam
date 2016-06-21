from build.transform.pybuild import CXXToolchain 
from build.tools import clang
from build.features.clang import PyBuildWordsize

macosx_x86 = CXXToolchain("macosx-x86-pybuild-clang")
macosx_x86.add_tool('.S', clang.PyBuildCXXCompiler(cxx=False))
macosx_x86.add_tool('.c', clang.PyBuildCXXCompiler(cxx=False))
macosx_x86.add_tool('.cc', clang.PyBuildCXXCompiler(cxx=True))
macosx_x86.add_tool('.cpp', clang.PyBuildCXXCompiler(cxx=True))
macosx_x86.add_tool('.cxx', clang.PyBuildCXXCompiler(cxx=True))
macosx_x86.archiver = clang.PyBuildCXXArchiver()
macosx_x86.linker = clang.PyBuildCXXLinker()
macosx_x86.add_feature(PyBuildWordsize(32))

macosx_x64 = CXXToolchain("macosx-x64-pybuild-clang")
macosx_x64.add_tool('.S', clang.PyBuildCXXCompiler(cxx=False))
macosx_x64.add_tool('.c', clang.PyBuildCXXCompiler(cxx=False))
macosx_x64.add_tool('.cc', clang.PyBuildCXXCompiler(cxx=True))
macosx_x64.add_tool('.cpp', clang.PyBuildCXXCompiler(cxx=True))
macosx_x64.add_tool('.cxx', clang.PyBuildCXXCompiler(cxx=True))
macosx_x64.archiver = clang.PyBuildCXXArchiver()
macosx_x64.linker = clang.PyBuildCXXLinker()
macosx_x64.add_feature(PyBuildWordsize(64))

