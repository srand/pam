import tempfile
import os
import re
import subprocess
from copy import copy



class Toolchain(object):
    def __init__(self):
        super(Toolchain, self).__init__()
        self._tools = {}

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


def win_x86_vs2015xp_settings():
    def create_env():
        env = copy(os.environ)
        
        installdir = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0'
        if not os.path.exists(installdir):
            raise RuntimeError('VS2015 is not installed')
        
        common7ide = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\Common7\IDE'
        vcbin = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN'
        common7tools = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\Common7\Tools'
        include = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE;C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE;C:\Program Files (x86)\Windows Kits\10\\include\10.0.10056.0\ucrt;C:\Program Files (x86)\Windows Kits\8.1\include\shared;C:\Program Files (x86)\Windows Kits\8.1\include\um;C:\Program Files (x86)\Windows Kits\8.1\include\winrt;'
        lib = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB;C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB;C:\Program Files (x86)\Windows Kits\10\\lib\10.0.10056.0\ucrt\x86;C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86;'
        libpath = r'C:\WINDOWS\Microsoft.NET\Framework\v4.0.30319;C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB;C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB;C:\Program Files (x86)\Windows Kits\8.1\References\CommonConfiguration\Neutral;\Microsoft.VCLibs\14.0\References\CommonConfiguration\neutral;'
        
        env['VSINSTALLDIR'] = installdir
        env['PATH'] = '{};{};{};{}'.format(common7ide, vcbin, common7tools, env['PATH'])
        env['VS140COMNTOOLS'] = common7tools
        env['INCLUDE'] = include 
        env['LIB'] = lib 
        env['LIBPATH'] = libpath 
        return env
    
    toolchain = MSVCCXXToolchain(create_env())
    return Settings(toolchain.settings)

"""