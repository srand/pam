##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


import sys
import os
import re
import platform
from build.utils import Loader


class ToolchainRegistry(object):
    _toolchains = {}
    
    @staticmethod
    def add(toolchain):
        ToolchainRegistry._toolchains[toolchain.name] = toolchain
        
    @staticmethod
    def find(toolchain):
        if toolchain not in ToolchainRegistry._toolchains:
            raise ValueError(toolchain) 
        return ToolchainRegistry._toolchains[toolchain]
        
    @staticmethod
    def names():
        return ToolchainRegistry._toolchains.keys()
        
    @staticmethod
    def all():
        return ToolchainRegistry._toolchains.values()

    @staticmethod
    def this_system():
        return [tc for tc in ToolchainRegistry._toolchains.values() 
                if re.search(platform.system().lower(), tc.name) and tc.supported]

class ToolchainLoader(Loader):
    def __init__(self, path):
        super(ToolchainLoader, self).__init__("build.toolchains", path)


class ToolchainAttributes(object):
    def __init__(self, toolchain):
        self.output = os.path.join("output", toolchain.name)


class Toolchain(object):
    def __init__(self, name):
        super(Toolchain, self).__init__()
        self._tools = {}
        self._features = []
        self._features_with_name = {}
        self._requirements = []
        self.name = name
        self.attributes = ToolchainAttributes(self)
        ToolchainRegistry.add(self)

    def add_feature(self, feature, name=None):
        if not name:
            # Anonymous features are applied to all projects
            self._features.append(feature)
        else:
            # while named features are optional and selected by the project
            self._features_with_name[name] = feature
            
    def apply_feature(self, project, transformed_project, toolchain, feature):
        if feature.matches(self.name):
            name, args = feature.name, feature.args
            feature = self._features_with_name.get(name)
            if feature:
                feature.transform(project, transformed_project, toolchain, **args)

    def apply_features(self, project, transformed_project, toolchain):
        # Apply toolchain features
        for feature in self._features:
            feature.transform(project, transformed_project, toolchain)
        # Apply project features
        for feature in project.features:
            self.apply_feature(project, transformed_project, toolchain, feature)

    def add_tool(self, extension, driver):
        self._tools[extension] = driver

    def get_tool(self, extension):
        if extension not in self._tools:
            raise RuntimeError('could not find tool for {} extension'.format(extension))
        return self._tools[extension]

    def add_requirement(self, req):
        self._requirements.append(req)

    @property
    def supported(self):
        return all([req.satisfied for req in self._requirements])

    def transform(self, project):
        pass


class ToolchainExtender(Toolchain):
    def __init__(self, name, toolchain):
        super(ToolchainExtender, self).__init__(name)
        self.toolchain = toolchain if isinstance(toolchain, Toolchain) else ToolchainRegistry.find(toolchain)
        self._used_features = []        

    @property
    def supported(self):
        return self.toolchain.supported and super(ToolchainExtender, self).supported

    def apply_features(self, project, transformed_project, toolchain):
        for feature in self._used_features:
            self.apply_feature(project, transformed_project, toolchain, feature)
        self.toolchain.apply_features(project, transformed_project, toolchain)
        super(ToolchainExtender, self).apply_features(project, transformed_project, toolchain)
        
    def use_feature(self, name):
        feature = Feature(name)
        self._used_features.append(feature)
        return feature    

    def get_tool(self, extension):
        try:
            return super(ToolchainExtender, self).get_tool(extension)
        except:
            pass
        return self.toolchain.get_tool(extension)

    def generate(self, project, toolchain=None):
        return self.toolchain.generate(project, toolchain)

    def transform(self, project):
        self.generate(project, self).transform()

