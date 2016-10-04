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


def _windows():
    return platform.system() == 'Windows'


class PyBuildCXXCompiler(gnu.PyBuildCXXCompiler):
    def __init__(self, cxx=False):
        super(PyBuildCXXCompiler, self).__init__(cxx=cxx)
        self._executable = 'clang' if not cxx else 'clang++'


class PyBuildCXXArchiver(gnu.PyBuildCXXArchiver):
    def __init__(self):
        super(PyBuildCXXArchiver, self).__init__()


class PyBuildCXXLinker(gnu.PyBuildCXXLinker):
    def __init__(self):
        super(PyBuildCXXLinker, self).__init__()
        self._executable = 'clang++'


class XcBuildCXXCompiler(Tool):
    def __init__(self, cxx=False):
        super(XcBuildCXXCompiler, self).__init__()
        self.cxx = cxx
        
    def transform(self, cxx_project, sources):
        bp = cxx_project.create_source_buildphase()
        fr_list = []
        for source in sources:
            sr = cxx_project.create_file_reference(
                cxx_project.FILE_TYPE_CPP if self.cxx else cxx_project.FILE_TYPE_C,
                source.path)
            fr_list.append(sr)
            bf = cxx_project.create_build_file(sr.reference)
            bp.files.append(bf.reference)
        return fr_list
