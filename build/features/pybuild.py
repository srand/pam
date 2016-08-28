from build.feature import Feature


class PyBuildCustomCFlag(Feature):
    def __init__(self, str):
        super(PyBuildCustomCFlag, self).__init__()
        self.str = str

    def transform(self, project, cxx_project, **kwargs):
        cxx_project.add_cflag(self.str)


class PyBuildCustomCXXFlag(Feature):
    def __init__(self, str):
        super(PyBuildCustomCXXFlag, self).__init__()
        self.str = str

    def transform(self, project, cxx_project, **kwargs):
        cxx_project.add_cxxflag(self.str)


class PyBuildCustomLinkerFlag(Feature):
    def __init__(self, str):
        super(PyBuildCustomLinkerFlag, self).__init__()
        self.str = str

    def transform(self, project, cxx_project, **kwargs):
        cxx_project.add_linkflag(self.str)


class PyBuildOptimize(Feature):
    MSVC = {'disable': '/O0', 'space': '/O1', 'speed': '/O2', 'full': '/O3'}
    GNU = {'disable': '-O0', 'space': '-O1', 'speed': '-O2', 'full': '-O3'}

    def __init__(self, levels):
        super(PyBuildOptimize, self).__init__()
        self.levels = levels

    def transform(self, project, cxx_project, **kwargs):
        if 'level' not in kwargs:
            raise ValueError('no "level" argument provided to optimize feature')
        if kwargs['level'] not in self.levels:
            raise ValueError('illegal "level" argument provided to optimize feature')
        value = self.levels[kwargs.get('level')]
        cxx_project.add_cflag(value)
        cxx_project.add_cxxflag(value)
