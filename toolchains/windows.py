from build.transform import msbuild 
from build.transform import pybuild
from build.transform import toolchain
from build.transform.toolchain import ToolchainExtender

from build.feature import Feature
from build.tools import msvc, clang
from build.features import FeatureError
from build.features.msbuild import *
from build.features.pybuild import *  
from build.transform.visual_studio import VS12VCVars, VS14VCVars, VS15VCVars
from build.requirement import HostRequirement, EnvRequirement, PathRequirement

import os

defaultlibs = [
    'd2d1',
    'd3d11',
    'dxgi',
    'windowscodecs',
    'dwrite',
    'dxguid',
    'xaudio2',
    'xinput',
    'mfcore',
    'mfplat',
    'mfreadwrite',
    'mfuuid',
    'user32',
    'shell32',
    'gdi32',
    'ole32',
    'oleaut32',
    'Advapi32'
]

_win_x86_vs12_env = VS12VCVars(arch="amd64_x86")
_win_x64_vs12_env = VS12VCVars(arch="amd64")
_win_x86_vs14_env = VS14VCVars(arch="amd64_x86")
_win_x64_vs14_env = VS14VCVars(arch="amd64")
_win_x86_vs15_env = VS15VCVars(arch="amd64_x86")
_win_x64_vs15_env = VS15VCVars(arch="amd64")


_vs12_env_req = EnvRequirement("VS120COMNTOOLS")
_vs14_env_req = EnvRequirement("VS120COMNTOOLS")
_vs12_path_req = PathRequirement(_win_x86_vs12_env._scripts)
_vs14_path_req = PathRequirement(_win_x86_vs14_env._scripts)
_vs15_path_req = PathRequirement(_win_x86_vs15_env._scripts)


win_cs_vs12_msbuild = msbuild.CSToolchain("windows-msbuild-vs12", vcvars=_win_x86_vs12_env)
win_cs_vs12_msbuild.add_tool('.cs', msvc.MSBuildCSCompiler())
win_cs_vs12_msbuild.add_tool('.png', msvc.MSBuildImage())
win_cs_vs12_msbuild.add_tool('.jpg', msvc.MSBuildImage())
win_cs_vs12_msbuild.add_tool('.bmp', msvc.MSBuildImage())
win_cs_vs12_msbuild.add_tool('.gif', msvc.MSBuildImage())
win_cs_vs12_msbuild.add_tool('.content', msvc.MSBuildContent())
win_cs_vs12_msbuild.add_requirement(HostRequirement.WINDOWS)
win_cs_vs12_msbuild.add_requirement(_vs12_env_req)
win_cs_vs12_msbuild.add_requirement(_vs12_path_req)

win_cs_vs14_msbuild = msbuild.CSToolchain("windows-msbuild-vs14", vcvars=_win_x86_vs14_env)
win_cs_vs14_msbuild.add_tool('.cs', msvc.MSBuildCSCompiler())
win_cs_vs14_msbuild.add_tool('.png', msvc.MSBuildImage())
win_cs_vs14_msbuild.add_tool('.jpg', msvc.MSBuildImage())
win_cs_vs14_msbuild.add_tool('.bmp', msvc.MSBuildImage())
win_cs_vs14_msbuild.add_tool('.gif', msvc.MSBuildImage())
win_cs_vs14_msbuild.add_tool('.content', msvc.MSBuildContent())
win_cs_vs14_msbuild.add_requirement(HostRequirement.WINDOWS)
win_cs_vs14_msbuild.add_requirement(_vs14_env_req)
win_cs_vs14_msbuild.add_requirement(_vs14_path_req)


win_x86_vs12_msbuild = msbuild.CXXToolchain("windows-x86-msbuild-vs12", platform="Win32", vcvars=_win_x86_vs12_env)
win_x86_vs12_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x86_vs12_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.add_tool('.png', msvc.MSBuildImage())
win_x86_vs12_msbuild.add_tool('.jpg', msvc.MSBuildImage())
win_x86_vs12_msbuild.add_tool('.bmp', msvc.MSBuildImage())
win_x86_vs12_msbuild.add_tool('.gif', msvc.MSBuildImage())
win_x86_vs12_msbuild.add_feature(MSBuildPlatformToolset(toolset='v120'))
win_x86_vs12_msbuild.add_requirement(HostRequirement.WINDOWS)
win_x86_vs12_msbuild.add_requirement(_vs12_env_req)
win_x86_vs12_msbuild.add_requirement(_vs12_path_req)
win_x86_vs12_msbuild.add_feature(FeatureError('c++11 is not supported by vs12'), 'language-c++11')
win_x86_vs12_msbuild.add_feature(FeatureError('c++14 is not supported by vs12'), 'language-c++14')
win_x86_vs12_msbuild.add_feature(FeatureError('c++17 is not supported by vs12'), 'language-c++17')
win_x86_vs12_msbuild.add_feature(MSBuildOptimize.MSVC, 'optimize')
win_x86_vs12_msbuild.add_feature(MSBuildProjectMacros.MSVC)
win_x86_vs12_msbuild.add_feature(MSBuildProjectIncPaths.MSVC)
win_x86_vs12_msbuild.add_feature(MSBuildProjectLibPaths.MSVC)
win_x86_vs12_msbuild.add_feature(MSBuildProjectDeps.MSVC)
win_x86_vs12_msbuild.add_feature(MSBuildProjectLibraries.MSVC)
win_x86_vs12_msbuild.add_feature(MSBuildLinkLibrary(defaultlibs))

win_x64_vs12_msbuild = msbuild.CXXToolchain("windows-x64-msbuild-vs12", vcvars=_win_x64_vs12_env)
win_x64_vs12_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x64_vs12_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.add_tool('.png', msvc.MSBuildImage())
win_x64_vs12_msbuild.add_tool('.jpg', msvc.MSBuildImage())
win_x64_vs12_msbuild.add_tool('.bmp', msvc.MSBuildImage())
win_x64_vs12_msbuild.add_tool('.gif', msvc.MSBuildImage())
win_x64_vs12_msbuild.add_feature(MSBuildPlatformToolset(toolset='v120'))
win_x64_vs12_msbuild.add_requirement(HostRequirement.WINDOWS)
win_x64_vs12_msbuild.add_requirement(_vs12_env_req)
win_x64_vs12_msbuild.add_requirement(_vs12_path_req)
win_x64_vs12_msbuild.add_feature(FeatureError('c++11 is not supported by vs12'), 'language-c++11')
win_x64_vs12_msbuild.add_feature(FeatureError('c++14 is not supported by vs12'), 'language-c++14')
win_x64_vs12_msbuild.add_feature(FeatureError('c++17 is not supported by vs12'), 'language-c++17')
win_x64_vs12_msbuild.add_feature(MSBuildOptimize.MSVC, 'optimize')
win_x64_vs12_msbuild.add_feature(MSBuildProjectMacros.MSVC)
win_x64_vs12_msbuild.add_feature(MSBuildProjectIncPaths.MSVC)
win_x64_vs12_msbuild.add_feature(MSBuildProjectLibPaths.MSVC)
win_x64_vs12_msbuild.add_feature(MSBuildProjectDeps.MSVC)
win_x64_vs12_msbuild.add_feature(MSBuildProjectLibraries.MSVC)
win_x64_vs12_msbuild.add_feature(MSBuildLinkLibrary(defaultlibs))



win_x86_vs14_msbuild = msbuild.CXXToolchain("windows-x86-msbuild-vs14", platform="Win32", vcvars=_win_x86_vs14_env)
win_x86_vs14_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x86_vs14_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs14_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs14_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs14_msbuild.add_tool('.png', msvc.MSBuildImage())
win_x86_vs14_msbuild.add_tool('.jpg', msvc.MSBuildImage())
win_x86_vs14_msbuild.add_tool('.bmp', msvc.MSBuildImage())
win_x86_vs14_msbuild.add_tool('.gif', msvc.MSBuildImage())
win_x86_vs14_msbuild.add_feature(MSBuildPlatformToolset(toolset='v140'))
win_x86_vs14_msbuild.add_requirement(HostRequirement.WINDOWS)
win_x86_vs14_msbuild.add_requirement(_vs14_env_req)
win_x86_vs14_msbuild.add_requirement(_vs14_path_req)
win_x86_vs14_msbuild.add_feature(FeatureError('c++14 is not supported by vs14'), 'language-c++14')
win_x86_vs14_msbuild.add_feature(FeatureError('c++17 is not supported by vs14'), 'language-c++17')
win_x86_vs14_msbuild.add_feature(MSBuildOptimize.MSVC, 'optimize')
win_x86_vs14_msbuild.add_feature(MSBuildProjectMacros.MSVC)
win_x86_vs14_msbuild.add_feature(MSBuildProjectIncPaths.MSVC)
win_x86_vs14_msbuild.add_feature(MSBuildProjectLibPaths.MSVC)
win_x86_vs14_msbuild.add_feature(MSBuildProjectDeps.MSVC)
win_x86_vs14_msbuild.add_feature(MSBuildProjectLibraries.MSVC)
win_x86_vs14_msbuild.add_feature(MSBuildLinkLibrary(defaultlibs))

win_x64_vs14_msbuild = msbuild.CXXToolchain("windows-x64-msbuild-vs14", vcvars=_win_x64_vs14_env)
win_x64_vs14_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x64_vs14_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs14_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs14_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs14_msbuild.add_tool('.png', msvc.MSBuildImage())
win_x64_vs14_msbuild.add_tool('.jpg', msvc.MSBuildImage())
win_x64_vs14_msbuild.add_tool('.bmp', msvc.MSBuildImage())
win_x64_vs14_msbuild.add_tool('.gif', msvc.MSBuildImage())
win_x64_vs14_msbuild.add_feature(MSBuildPlatformToolset(toolset='v140'))
win_x64_vs14_msbuild.add_requirement(HostRequirement.WINDOWS)
win_x64_vs14_msbuild.add_requirement(_vs14_env_req)
win_x64_vs14_msbuild.add_requirement(_vs14_path_req)
win_x64_vs14_msbuild.add_feature(FeatureError('c++14 is not supported by vs14'), 'language-c++14')
win_x64_vs14_msbuild.add_feature(FeatureError('c++17 is not supported by vs14'), 'language-c++17')
win_x64_vs14_msbuild.add_feature(MSBuildOptimize.MSVC, 'optimize')
win_x64_vs14_msbuild.add_feature(MSBuildProjectMacros.MSVC)
win_x64_vs14_msbuild.add_feature(MSBuildProjectIncPaths.MSVC)
win_x64_vs14_msbuild.add_feature(MSBuildProjectLibPaths.MSVC)
win_x64_vs14_msbuild.add_feature(MSBuildProjectDeps.MSVC)
win_x64_vs14_msbuild.add_feature(MSBuildProjectLibraries.MSVC)
win_x64_vs14_msbuild.add_feature(MSBuildLinkLibrary(defaultlibs))



win_x86_vs15_msbuild = msbuild.CXXToolchain("windows-x86-msbuild-vs15", platform="Win32", vcvars=_win_x86_vs15_env)
win_x86_vs15_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x86_vs15_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs15_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs15_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs15_msbuild.add_tool('.png', msvc.MSBuildImage())
win_x86_vs15_msbuild.add_tool('.jpg', msvc.MSBuildImage())
win_x86_vs15_msbuild.add_tool('.bmp', msvc.MSBuildImage())
win_x86_vs15_msbuild.add_tool('.gif', msvc.MSBuildImage())
win_x86_vs15_msbuild.add_feature(MSBuildPlatformToolset(toolset='v141'))
win_x86_vs15_msbuild.add_requirement(HostRequirement.WINDOWS)
win_x86_vs15_msbuild.add_requirement(_vs15_path_req)
win_x86_vs15_msbuild.add_feature(FeatureError('c++14 is not supported by vs15'), 'language-c++14')
win_x86_vs15_msbuild.add_feature(FeatureError('c++17 is not supported by vs15'), 'language-c++17')
win_x86_vs15_msbuild.add_feature(MSBuildOptimize.MSVC, 'optimize')
win_x86_vs15_msbuild.add_feature(MSBuildProjectMacros.MSVC)
win_x86_vs15_msbuild.add_feature(MSBuildProjectIncPaths.MSVC)
win_x86_vs15_msbuild.add_feature(MSBuildProjectLibPaths.MSVC)
win_x86_vs15_msbuild.add_feature(MSBuildProjectDeps.MSVC)
win_x86_vs15_msbuild.add_feature(MSBuildProjectLibraries.MSVC)
win_x86_vs15_msbuild.add_feature(MSBuildLinkLibrary(defaultlibs))

win_x64_vs15_msbuild = msbuild.CXXToolchain("windows-x64-msbuild-vs15", vcvars=_win_x64_vs15_env)
win_x64_vs15_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x64_vs15_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs15_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs15_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs15_msbuild.add_tool('.png', msvc.MSBuildImage())
win_x64_vs15_msbuild.add_tool('.jpg', msvc.MSBuildImage())
win_x64_vs15_msbuild.add_tool('.bmp', msvc.MSBuildImage())
win_x64_vs15_msbuild.add_tool('.gif', msvc.MSBuildImage())
win_x64_vs15_msbuild.add_feature(MSBuildPlatformToolset(toolset='v141'))
win_x64_vs15_msbuild.add_requirement(HostRequirement.WINDOWS)
win_x64_vs15_msbuild.add_requirement(_vs15_path_req)
win_x64_vs15_msbuild.add_feature(FeatureError('c++14 is not supported by vs15'), 'language-c++14')
win_x64_vs15_msbuild.add_feature(FeatureError('c++17 is not supported by vs15'), 'language-c++17')
win_x64_vs15_msbuild.add_feature(MSBuildOptimize.MSVC, 'optimize')
win_x64_vs15_msbuild.add_feature(MSBuildProjectMacros.MSVC)
win_x64_vs15_msbuild.add_feature(MSBuildProjectIncPaths.MSVC)
win_x64_vs15_msbuild.add_feature(MSBuildProjectLibPaths.MSVC)
win_x64_vs15_msbuild.add_feature(MSBuildProjectDeps.MSVC)
win_x64_vs15_msbuild.add_feature(MSBuildProjectLibraries.MSVC)
win_x64_vs15_msbuild.add_feature(MSBuildLinkLibrary(defaultlibs))



pam_vs12 = pybuild.CXXToolchain("pam-vs12")
pam_vs12.add_requirement(HostRequirement.WINDOWS)
pam_vs12.add_requirement(_vs12_env_req)
pam_vs12.add_requirement(_vs12_path_req)
pam_vs12.add_feature(FeatureError('c++11 is not supported by vs12'), 'language-c++11')
pam_vs12.add_feature(FeatureError('c++14 is not supported by vs12'), 'language-c++14')
pam_vs12.add_feature(FeatureError('c++17 is not supported by vs12'), 'language-c++17')
pam_vs12.add_feature(PyBuildOptimize.MSVC, 'optimize')
pam_vs12.add_feature(PyBuildProjectMacros.MSVC)
pam_vs12.add_feature(PyBuildProjectIncPaths.MSVC)
pam_vs12.add_feature(PyBuildProjectLibPaths.MSVC)
pam_vs12.add_feature(PyBuildProjectDeps.MSVC)
pam_vs12.add_feature(PyBuildProjectLibraries.MSVC)
pam_vs12.add_feature(PyBuildLinkLibrary(defaultlibs))
pam_vs12.add_feature(PyBuildCustomLinkerFlag('/subsystem:console'))

win_x86_vs12 = ToolchainExtender("windows-x86-pam-vs12", pam_vs12)
win_x86_vs12.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs12_env))
win_x86_vs12.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs12_env)
win_x86_vs12.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs12_env)

win_x64_vs12 = ToolchainExtender("windows-x64-pam-vs12", pam_vs12)
win_x64_vs12.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs12_env))
win_x64_vs12.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs12_env)
win_x64_vs12.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs12_env)



pam_vs14 = pybuild.CXXToolchain("pam-vs14")
pam_vs14.add_requirement(HostRequirement.WINDOWS)
pam_vs14.add_requirement(_vs14_env_req)
pam_vs14.add_requirement(_vs14_path_req)
pam_vs14.add_feature(FeatureError('c++14 is not supported by vs12'), 'language-c++14')
pam_vs14.add_feature(FeatureError('c++17 is not supported by vs12'), 'language-c++17')
pam_vs14.add_feature(PyBuildOptimize.MSVC, 'optimize')
pam_vs14.add_feature(PyBuildProjectMacros.MSVC)
pam_vs14.add_feature(PyBuildProjectIncPaths.MSVC)
pam_vs14.add_feature(PyBuildProjectLibPaths.MSVC)
pam_vs14.add_feature(PyBuildProjectDeps.MSVC)
pam_vs14.add_feature(PyBuildProjectLibraries.MSVC)
pam_vs14.add_feature(PyBuildLinkLibrary(defaultlibs))
pam_vs14.add_feature(PyBuildCustomLinkerFlag('/subsystem:console'))


win_x86_vs14 = ToolchainExtender("windows-x86-pam-vs14", pam_vs14)
win_x86_vs14.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs14_env)
win_x86_vs14.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs14_env)

win_x64_vs14 = ToolchainExtender("windows-x64-pam-vs14", pam_vs14)
win_x64_vs14.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs14_env)
win_x64_vs14.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs14_env)



pam_vs15 = pybuild.CXXToolchain("pam-vs15")
pam_vs15.add_requirement(HostRequirement.WINDOWS)
pam_vs15.add_requirement(_vs15_path_req)
pam_vs15.add_feature(FeatureError('c++14 is not supported by vs12'), 'language-c++14')
pam_vs15.add_feature(FeatureError('c++17 is not supported by vs12'), 'language-c++17')
pam_vs15.add_feature(PyBuildOptimize.MSVC, 'optimize')
pam_vs15.add_feature(PyBuildProjectMacros.MSVC)
pam_vs15.add_feature(PyBuildProjectIncPaths.MSVC)
pam_vs15.add_feature(PyBuildProjectLibPaths.MSVC)
pam_vs15.add_feature(PyBuildProjectDeps.MSVC)
pam_vs15.add_feature(PyBuildProjectLibraries.MSVC)
pam_vs15.add_feature(PyBuildLinkLibrary(defaultlibs))
pam_vs15.add_feature(PyBuildCustomLinkerFlag('/subsystem:console'))


win_x86_vs15 = ToolchainExtender("windows-x86-pam-vs15", pam_vs15)
win_x86_vs15.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs15_env))
win_x86_vs15.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs15_env))
win_x86_vs15.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs15_env))
win_x86_vs15.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs15_env))
win_x86_vs15.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs15_env))
win_x86_vs15.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs15_env)
win_x86_vs15.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs15_env)

win_x64_vs15 = ToolchainExtender("windows-x64-pam-vs15", pam_vs15)
win_x64_vs15.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs15_env))
win_x64_vs15.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs15_env))
win_x64_vs15.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs15_env))
win_x64_vs15.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs15_env))
win_x64_vs15.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs15_env))
win_x64_vs15.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs15_env)
win_x64_vs15.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs15_env)


vs14_clang = pybuild.CXXToolchain("pam-clang-vs14")
clang.ClangToolFactory().configure(vs14_clang)
vs14_clang.add_requirement(HostRequirement.WINDOWS)
vs14_clang.add_requirement(_vs14_env_req)
vs14_clang.add_requirement(_vs14_path_req)
vs14_clang.add_feature(PyBuildCustomCFlag('-m32'))
vs14_clang.add_feature(PyBuildCustomCXXFlag('-m32'))
vs14_clang.add_feature(PyBuildCustomLinkerFlag('-m32'))
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c89'), 'language-c89')
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c99'), 'language-c99')
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c11'), 'language-c11')
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c++11'), 'language-c++11')
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c++14'), 'language-c++14')
vs14_clang.add_feature(PyBuildCustomCXXFlag('-std=c++17'), 'language-c++17')
vs14_clang.add_feature(PyBuildOptimize.GNU, 'optimize')
vs14_clang.add_feature(PyBuildProjectMacros.GNU)
vs14_clang.add_feature(PyBuildProjectIncPaths.GNU)
vs14_clang.add_feature(PyBuildProjectLibPaths.GNU)
vs14_clang.add_feature(PyBuildProjectDeps.MSVC)
vs14_clang.add_feature(PyBuildProjectLibraries.GNU)

win_x86_vs14_clang = ToolchainExtender("windows-x86-pam-clang-vs14", vs14_clang)
win_x86_vs14_clang.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs14_env)
win_x86_vs14_clang.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs14_env)

win_x64_vs14_clang = ToolchainExtender("windows-x64-pam-clang-vs14", vs14_clang)
win_x64_vs14_clang.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs14_env)
win_x64_vs14_clang.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs14_env)
