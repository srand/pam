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
