from build.transform import pybuild
from build.tools import Tool
import platform


class _Directory(pybuild.Command):
    def __init__(self, dirname):
        if platform.system() == "Windows":
            cmdline = "cmd /c if not exist \"{dir}\" mkdir \"{dir}\"".format(dir=dirname)
        else:
            cmdline = "mkdir -p \"{dir}\"".format(dir=dirname)
        info = '[MKDIR] {}'.format(dirname)
        super(_Directory, self).__init__(dirname, cmdline, info)


class PyBuildDirectoryCreator(Tool):
    def __init__(self):
        super(PyBuildDirectoryCreator, self).__init__()

    def transform(self, cxx_project, dirname):
        job = cxx_project.get_job(dirname)
        if not job:
            job = _Directory(dirname)
            cxx_project.add_job(job)
        return job
