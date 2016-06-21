

class PyBuildOptimize:
    NONE = 0
    SIZE = 1
    SPEED = 2
    FULL = 3

    def __init__(self, level=FULL):
        self.level = level

    def transform(self, project, cxx_project):
        value = ['/O0', '/O1', '/O2', '/O3'][self.level]
        cxx_project.add_cflag(value)
        cxx_project.add_cxxflag(value)


class PyBuildWordsize:
    def __init__(self, bits):
        self.bits = bits

    def transform(self, project, cxx_project):
        value = '-m{}'.format(self.bits)
        cxx_project.add_cflag(value)
        cxx_project.add_cxxflag(value)
        cxx_project.add_linkflag(value)
