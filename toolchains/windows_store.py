from build.transform import msbuild 
from build.transform.visual_studio import VS12VCVars, VS14VCVars

winstore_x86 = msbuild.CXXToolchain("windows-store-x86-vs12-msbuild", VS12VCVars(host="x64", target="x86", store=True))
winstore_x86.platform = "Win32"
winstore_x86.toolset = "v120"
winstore_x86.globals.applicationtype = "Windows Store"
winstore_x86.globals.applicationtyperevision = "8.1"
winstore_x86.globals.appcontainerapplication = "true"
winstore_x86.clcompile.precompiledheader = "NotUsing"

winstore_x86 = msbuild.CXXToolchain("windows-store-arm-vs12-msbuild", VS12VCVars(host="x64", target="arm", store=True))
winstore_x86.platform = "ARM"
winstore_x86.toolset = "v120"
winstore_x86.globals.applicationtype = "Windows Store"
winstore_x86.globals.applicationtyperevision = "8.1"
winstore_x86.globals.appcontainerapplication = "true"
winstore_x86.clcompile.precompiledheader = "NotUsing"
