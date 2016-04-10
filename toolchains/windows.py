from build.transform import msbuild 
from build.transform import native
from build.transform.visual_studio import VS12VCVars, VS14VCVars


win_x86_vs12_msbuild = msbuild.CXXToolchain("windows-x86-vs12-msbuild", VS12VCVars(host="x64", target="x86"))
win_x86_vs12_msbuild.platform = "Win32"
win_x86_vs12_msbuild.toolset = "v120_xp"
win_x86_vs12_msbuild.charset = "MultiByte"

win_x64_vs12_msbuild = msbuild.CXXToolchain("windows-x64-vs12-msbuild", VS12VCVars(host="x64", target="x64"))
win_x64_vs12_msbuild.platform = "x64"
win_x64_vs12_msbuild.toolset = "v120_xp"
win_x64_vs12_msbuild.charset = "MultiByte"

win_x86_vs12 = native.MSVCCXXToolchain("windows-x86-vs12", VS14VCVars(host="x64", target="x86"))
win_x86_vs12.add_linkflag('/subsystem:console')

win_x64_vs12 = native.MSVCCXXToolchain("windows-x64-vs12", VS14VCVars(host="x64", target="x64"))
win_x64_vs12.add_linkflag('/subsystem:console')

#win_x86_vs14 = msbuild.CXXToolchain("windows-x86-vs14-msbuild", VS14VCVars(host="x64", target="x86"))
#win_x86_vs14.platform = "Win32"
#win_x86_vs14.toolset = "v140"
#win_x86_vs14.charset = "MultiByte"

#win_x64_vs14 = msbuild.CXXToolchain("windows-x64-vs15-msbuild", VS14VCVars(host="x64", target="x64"))
#win_x64_vs14.platform = "x64"
#win_x64_vs14.toolset = "v140"
#win_x64_vs14.charset = "MultiByte"
