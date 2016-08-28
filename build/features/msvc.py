from build.features.pybuild import * 

class PyBuildOptimize(PyBuildCustomCFlag, PyBuildCustomCXXFlag):
    NONE = 0
    SIZE = 1
    SPEED = 2
    FULL = 3

    def __init__(self, level=FULL):
        super(PyBuildOptimize, self).__init__(['/Od', '/O1', '/O2', '/Ox'][level])
        self.level = level

###############################################################################

class MSBuildOptimize:
    NONE = 0
    SIZE = 1
    SPEED = 2
    FULL = 3

    def __init__(self, level=FULL):
        self.level = level

    def transform(self, project, cxx_project):
        value = ['Disabled', 'MinSpace', 'MaxSpeed', 'Full'][self.level]
        cxx_project.clcompile.optimize = value 


class MSBuildPlatformToolset:
    def __init__(self, toolset='v140', charset='MultiByte'):
        self.toolset = toolset
        self.charset = charset

    def transform(self, project, cxx_project):
        cxx_project.config_props.toolset = self.toolset
        cxx_project.config_props.charset = self.charset
