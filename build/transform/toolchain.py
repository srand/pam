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
        return [tc for tc in ToolchainRegistry._toolchains.values() if re.search(platform.system().lower(), tc.name)]


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
        self._requirements = []
        self.name = name
        self.attributes = ToolchainAttributes(self)
        ToolchainRegistry.add(self)

    def add_feature(self, feature):
        self._features.append(feature)

    def apply_features(self, project, transformed_project):
        for feature in self._features:
            feature.transform(project, transformed_project)

    def add_tool(self, extension, driver):
        self._tools[extension] = driver

    def get_tool(self, extension):
        if extension not in self._tools:
            raise RuntimeError('could not find tool for extension {}'.format(extension))
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
        self.toolchain = toolchain

    @property
    def attribute(self):
        return self.toolchain.attributes

    def apply_features(self, project, transformed_project):
        self.toolchain.apply_features(project, transformed_project)
        super(ToolchainExtender, self).apply_features(project, transformed_project)

    def get_tool(self, extension):
        try:
            return super(ToolchainExtender, self).get_tool(extension)
        except:
            pass
        return self.toolchain.get_Tool(extension)

    def generate(self, project, toolchain=None):
        return self.toolchain.generate(project, toolchain)

    def transform(self, project):
        self.generate(project, self).transform()

"""        
def mac_x86_libcxx_settings():
    toolchain = ClangCXXToolchain()
    toolchain.settings.add_cflag('-m32')
    toolchain.settings.add_cxxflag('-m32')
    toolchain.settings.add_cxxflag('-stdlib=libc++')
    toolchain.settings.add_linkflag('-m32')
    toolchain.settings.add_linkflag('-stdlib=libc++')
    return Settings(toolchain.settings)


def ios_x86_libcxx_settings():
    toolchain = ClangCXXToolchain()
    toolchain.settings.add_cflag('-m32')
    toolchain.settings.add_cxxflag('-m32')
    toolchain.settings.add_cxxflag('-stdlib=libc++')
    toolchain.settings.add_linkflag('-m32')
    toolchain.settings.add_linkflag('-stdlib=libc++')

    toolchain.settings.add_cflag('-isysroot')
    toolchain.settings.add_cflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    toolchain.settings.add_cxxflag('-isysroot')
    toolchain.settings.add_cxxflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    toolchain.settings.add_linkflag('-isysroot')
    toolchain.settings.add_linkflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    return Settings(toolchain.settings)


def ios_armv7_libcxx_settings():
    toolchain = ClangCXXToolchain()

    # Building for ARMv7
    toolchain.settings.add_cflag('-arch', 'armv7')
    toolchain.settings.add_cxxflag('-arch', 'armv7')
    toolchain.settings.add_linkflag('-arch', 'armv7')

    # With libc++
    toolchain.settings.add_cxxflag('-stdlib=libc++')
    toolchain.settings.add_linkflag('-stdlib=libc++')

    # And default iOS SDK
    toolchain.settings.add_cflag('-isysroot')
    toolchain.settings.add_cflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    toolchain.settings.add_cxxflag('-isysroot')
    toolchain.settings.add_cxxflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    toolchain.settings.add_linkflag('-isysroot')
    toolchain.settings.add_linkflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    return Settings(toolchain.settings)

"""