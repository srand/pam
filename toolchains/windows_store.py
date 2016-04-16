from build.transform import msbuild 
from build.transform.visual_studio import VS12VCVars, VS14VCVars
from build.tools import msvc


winstore_x86 = msbuild.CXXToolchain("windows-store-x86-msbuild-vs12", VS12VCVars(host="x64", target="x86", store=True))
winstore_x86.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
winstore_x86.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
winstore_x86.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
winstore_x86.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
winstore_x86.platform = "Win32"
winstore_x86.toolset = "v120"
winstore_x86.globals.applicationtype = "Windows Store"
winstore_x86.globals.applicationtyperevision = "8.1"
winstore_x86.globals.appcontainerapplication = "true"
winstore_x86.clcompile.precompiledheader = "NotUsing"


winstore_arm = msbuild.CXXToolchain("windows-store-arm-msbuild-vs12", VS12VCVars(host="x64", target="arm", store=True))
winstore_arm.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
winstore_arm.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
winstore_arm.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
winstore_arm.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
winstore_arm.platform = "ARM"
winstore_arm.toolset = "v120"
winstore_arm.globals.applicationtype = "Windows Store"
winstore_arm.globals.applicationtyperevision = "8.1"
winstore_arm.globals.appcontainerapplication = "true"
winstore_arm.clcompile.precompiledheader = "NotUsing"
