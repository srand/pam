class PyBuildCustomCFlag(object):
    def __init__(self, str):
        super(PyBuildCustomCFlag, self).__init__()
        self.str = str

    def transform(self, project, cxx_project):
        cxx_project.add_cflag(self.str)


class PyBuildCustomCXXFlag(object):
    def __init__(self, str):
        super(PyBuildCustomCXXFlag, self).__init__()
        self.str = str

    def transform(self, project, cxx_project):
        cxx_project.add_cxxflag(self.str)


class PyBuildCustomLinkerFlag(object):
    def __init__(self, str):
        super(PyBuildCustomLinkerFlag, self).__init__()
        self.str = str

    def transform(self, project, cxx_project):
        cxx_project.add_linkflag(self.str)
