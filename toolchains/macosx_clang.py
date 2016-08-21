from build.transform.pybuild import CXXToolchain 
from build.tools import clang
from build.features.clang import PyBuildWordsize
from build.requirement import HostRequirement

macosx = CXXToolchain("macosx-pam-clang")
macosx.add_tool('.S', clang.PyBuildCXXCompiler(cxx=False))
macosx.add_tool('.c', clang.PyBuildCXXCompiler(cxx=False))
macosx.add_tool('.cc', clang.PyBuildCXXCompiler(cxx=True))
macosx.add_tool('.cpp', clang.PyBuildCXXCompiler(cxx=True))
macosx.add_tool('.cxx', clang.PyBuildCXXCompiler(cxx=True))
macosx.archiver = clang.PyBuildCXXArchiver()
macosx.linker = clang.PyBuildCXXLinker()
macosx.add_feature(PyBuildWordsize(32))
macosx.add_requirement(HostRequirement.DARWIN)

macosx_x86 = CXXToolchain("macosx-x86-pam-clang")
macosx_x86.add_tool('.S', clang.PyBuildCXXCompiler(cxx=False))
macosx_x86.add_tool('.c', clang.PyBuildCXXCompiler(cxx=False))
macosx_x86.add_tool('.cc', clang.PyBuildCXXCompiler(cxx=True))
macosx_x86.add_tool('.cpp', clang.PyBuildCXXCompiler(cxx=True))
macosx_x86.add_tool('.cxx', clang.PyBuildCXXCompiler(cxx=True))
macosx_x86.archiver = clang.PyBuildCXXArchiver()
macosx_x86.linker = clang.PyBuildCXXLinker()
macosx_x86.add_feature(PyBuildWordsize(32))
macosx_x86.add_requirement(HostRequirement.DARWIN)

macosx_x64 = CXXToolchain("macosx-x64-pam-clang")
macosx_x64.add_tool('.S', clang.PyBuildCXXCompiler(cxx=False))
macosx_x64.add_tool('.c', clang.PyBuildCXXCompiler(cxx=False))
macosx_x64.add_tool('.cc', clang.PyBuildCXXCompiler(cxx=True))
macosx_x64.add_tool('.cpp', clang.PyBuildCXXCompiler(cxx=True))
macosx_x64.add_tool('.cxx', clang.PyBuildCXXCompiler(cxx=True))
macosx_x64.archiver = clang.PyBuildCXXArchiver()
macosx_x64.linker = clang.PyBuildCXXLinker()
macosx_x64.add_feature(PyBuildWordsize(64))
macosx_x64.add_requirement(HostRequirement.DARWIN)
