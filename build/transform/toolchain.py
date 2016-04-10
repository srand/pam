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


class Toolchain(object):
    def __init__(self, name):
        super(Toolchain, self).__init__()
        self._tools = {}
        self.name = name
        ToolchainRegistry.add(self)

    def transform(self, project):
        pass


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