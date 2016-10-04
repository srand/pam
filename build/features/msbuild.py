##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


class MSBuildOptimize:
    def __init__(self):
        self.levels = {'disable': 'Disabled', 'space': 'MinSpace', 'speed': 'MaxSpeed', 'full': 'Full'}

    def transform(self, project, cxx_project, **kwargs):
        if 'level' not in kwargs:
            raise ValueError('no "level" argument provided to optimize feature')
        if kwargs['level'] not in self.levels:
            raise ValueError('illegal "level" argument provided to optimize feature')
        value = self.levels[kwargs.get('level')]
        cxx_project.clcompile.optimize = value 


class MSBuildPlatformToolset:
    def __init__(self, toolset='v140', charset='MultiByte'):
        self.toolset = toolset
        self.charset = charset

    def transform(self, project, cxx_project, **kwargs):
        cxx_project.config_props.toolset = self.toolset
        cxx_project.config_props.charset = self.charset
