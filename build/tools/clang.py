##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


from build.tools import Tool
from build.tools import gnu
from build.tools import msvc
import platform


class XcBuildCXXCompiler(Tool):
    def __init__(self, filetype='c++'):
        super(XcBuildCXXCompiler, self).__init__()
        self.filetype = filetype
        
    def transform(self, cxx_project, sources):
        bp = cxx_project.create_source_buildphase()
        fr_list = []
        for source in sources:
            sr = cxx_project.create_file_reference(
                cxx_project.FILE_TYPE_CPP if self.filetype == 'c++' else cxx_project.FILE_TYPE_C,
                source.path)
            fr_list.append(sr)
            bf = cxx_project.create_build_file(sr.reference)
            bp.files.append(bf.reference)
        return fr_list


class ClangToolFactory:
    def __init__(self, prefix=None, path=None):
        self.prefix = prefix
        self.path = path

    def configure(self, toolchain):
        toolchain.add_tool('.s', gnu.PyBuildCXXCompiler('clang', 'assembler', prefix=self.prefix, path=self.path))
        toolchain.add_tool('.S', gnu.PyBuildCXXCompiler('clang', 'assembler-with-cpp', prefix=self.prefix, path=self.path))
        toolchain.add_tool('.c', gnu.PyBuildCXXCompiler('clang', 'c', prefix=self.prefix, path=self.path))
        toolchain.add_tool('.cc', gnu.PyBuildCXXCompiler('clang++', 'c++', prefix=self.prefix, path=self.path))
        toolchain.add_tool('.cpp', gnu.PyBuildCXXCompiler('clang++', 'c++', prefix=self.prefix, path=self.path))
        toolchain.add_tool('.cxx', gnu.PyBuildCXXCompiler('clang++', 'c++', prefix=self.prefix, path=self.path))
        toolchain.archiver = gnu.PyBuildCXXArchiver(prefix=self.prefix, path=self.path)
        toolchain.linker = gnu.PyBuildCXXLinker(executable='clang++', prefix=self.prefix, path=self.path)
