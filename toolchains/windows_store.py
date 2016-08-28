from build.transform import msbuild 
from build.transform.visual_studio import VS12VCVars, VS14VCVars
from build.tools import msvc
from build.requirement import HostRequirement
from build.features import FeatureError
from build.features.msbuild import *


def PlatformToolset(platform='Win32', toolset='v140', charset='MultiByte'):
    class _PlatformToolset:
        def transform(self, project, cxx_project):
            cxx_project.globals_group.platform = platform
            cxx_project.config_props.toolset = toolset
            cxx_project.config_props.charset = charset
    return _PlatformToolset()


def StoreApp(revision='10.0', platform_revision=None):
    class _StoreApp:
        def transform(self, project, cxx_project):
            cxx_project.globals_group.applicationtype = "Windows Store"
            cxx_project.globals_group.applicationtyperevision = revision
            cxx_project.globals_group.appcontainerapplication = "true"
            if platform_revision:
                cxx_project.globals_group.windowstargetplatformversion = platform_revision
                cxx_project.globals_group.windowstargetplatformminversion = platform_revision
    return _StoreApp()


def NoPrecompiledHeader():
    class _PrecompiledHeader:
        def transform(self, project, cxx_project):
            cxx_project.clcompile.precompiledheader = "NotUsing"
    return _PrecompiledHeader()


winstore_x86_vs12 = msbuild.CXXToolchain("windows-store-x86-msbuild-vs12", vcvars=VS12VCVars(host="x64", target="x86", store=True, sdkver='8.1'))
winstore_x86_vs12.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
winstore_x86_vs12.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
winstore_x86_vs12.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
winstore_x86_vs12.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
winstore_x86_vs12.add_tool('.hlsl', msvc.MSBuildShaderCompiler())
winstore_x86_vs12.add_tool('.png', msvc.MSBuildImage())
winstore_x86_vs12.add_tool('.dds', msvc.MSBuildImage())
winstore_x86_vs12.add_tool('.wav', msvc.MSBuildMedia())
winstore_x86_vs12.add_tool('.appxmanifest', msvc.MSBuildAppxManifest())
winstore_x86_vs12.add_feature(PlatformToolset(toolset='v120'))
winstore_x86_vs12.add_feature(StoreApp(revision='8.1'))
winstore_x86_vs12.add_feature(NoPrecompiledHeader())
winstore_x86_vs12.add_feature(MSBuildOptimize(), 'optimize')
winstore_x86_vs12.add_requirement(HostRequirement.WINDOWS)


winstore_arm_vs12 = msbuild.CXXToolchain("windows-store-arm-msbuild-vs12", platform='ARM', vcvars=VS12VCVars(host="x64", target="arm", store=True, sdkver='8.1'))
winstore_arm_vs12.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
winstore_arm_vs12.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
winstore_arm_vs12.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
winstore_arm_vs12.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
winstore_arm_vs12.add_tool('.hlsl', msvc.MSBuildShaderCompiler())
winstore_arm_vs12.add_tool('.png', msvc.MSBuildImage())
winstore_arm_vs12.add_tool('.dds', msvc.MSBuildImage())
winstore_arm_vs12.add_tool('.wav', msvc.MSBuildMedia())
winstore_arm_vs12.add_tool('.appxmanifest', msvc.MSBuildAppxManifest())
winstore_arm_vs12.add_feature(PlatformToolset(toolset='v120'))
winstore_arm_vs12.add_feature(StoreApp(revision='8.1'))
winstore_arm_vs12.add_feature(NoPrecompiledHeader())
winstore_arm_vs12.add_feature(MSBuildOptimize(), 'optimize')
winstore_arm_vs12.add_requirement(HostRequirement.WINDOWS)


winstore_x86_vs14 = msbuild.CXXToolchain("windows-store-x86-msbuild-vs14", vcvars=VS14VCVars(host="x64", target="x86", store=True))
winstore_x86_vs14.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
winstore_x86_vs14.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
winstore_x86_vs14.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
winstore_x86_vs14.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
winstore_x86_vs14.add_tool('.hlsl', msvc.MSBuildShaderCompiler())
winstore_x86_vs14.add_tool('.png', msvc.MSBuildImage())
winstore_x86_vs14.add_tool('.dds', msvc.MSBuildImage())
winstore_x86_vs14.add_tool('.wav', msvc.MSBuildMedia())
winstore_x86_vs14.add_tool('.appxmanifest', msvc.MSBuildAppxManifest())
winstore_x86_vs14.add_feature(PlatformToolset(toolset='v140', charset=None))
winstore_x86_vs14.add_feature(StoreApp(revision='10.0', platform_revision='10.0.10586.0'))
winstore_x86_vs14.add_feature(NoPrecompiledHeader())
winstore_x86_vs14.add_feature(FeatureError('c++14 is not supported by vs14'), 'c++14')
winstore_x86_vs14.add_feature(FeatureError('c++17 is not supported by vs14'), 'c++17')
winstore_x86_vs14.add_feature(MSBuildOptimize(), 'optimize')
winstore_x86_vs14.add_requirement(HostRequirement.WINDOWS)


winstore_arm_vs14 = msbuild.CXXToolchain("windows-store-arm-msbuild-vs14", platform='ARM', vcvars=VS14VCVars(host="x64", target="arm", store=True))
winstore_arm_vs14.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
winstore_arm_vs14.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
winstore_arm_vs14.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
winstore_arm_vs14.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
winstore_arm_vs14.add_tool('.hlsl', msvc.MSBuildShaderCompiler())
winstore_arm_vs14.add_tool('.png', msvc.MSBuildImage())
winstore_arm_vs14.add_tool('.dds', msvc.MSBuildImage())
winstore_arm_vs14.add_tool('.wav', msvc.MSBuildMedia())
winstore_arm_vs14.add_tool('.appxmanifest', msvc.MSBuildAppxManifest())
winstore_arm_vs14.add_feature(PlatformToolset(toolset='v140', charset=None))
winstore_arm_vs14.add_feature(StoreApp(revision='10.0', platform_revision='10.0.10586.0'))
winstore_arm_vs14.add_feature(NoPrecompiledHeader())
winstore_arm_vs14.add_feature(FeatureError('c++14 is not supported by vs14'), 'c++14')
winstore_arm_vs14.add_feature(FeatureError('c++17 is not supported by vs14'), 'c++17')
winstore_arm_vs14.add_feature(MSBuildOptimize(), 'optimize')
winstore_arm_vs14.add_requirement(HostRequirement.WINDOWS)
