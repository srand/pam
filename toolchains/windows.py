from build.transform import msbuild 
from build.transform import pybuild
from build.tools import msvc, clang
from build.transform.visual_studio import VS12VCVars, VS14VCVars


_win_x86_vs12_env = VS12VCVars(host="x64", target="x86")
_win_x64_vs12_env = VS12VCVars(host="x64", target="x64")
_win_x86_vs14_env = VS14VCVars(host="x64", target="x86")
_win_x64_vs14_env = VS14VCVars(host="x64", target="x64")


win_x86_vs12_msbuild = msbuild.CXXToolchain("windows-x86-msbuild-vs12", _win_x86_vs12_env)
win_x86_vs12_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x86_vs12_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.platform = "Win32"
win_x86_vs12_msbuild.toolset = "v120_xp"
win_x86_vs12_msbuild.charset = "MultiByte"


win_x64_vs12_msbuild = msbuild.CXXToolchain("windows-x64-msbuild-vs12", _win_x86_vs12_env)
win_x64_vs12_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x64_vs12_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.platform = "x64"
win_x64_vs12_msbuild.toolset = "v120_xp"
win_x64_vs12_msbuild.charset = "MultiByte"


win_x86_vs12 = pybuild.CXXToolchain("windows-x86-pybuild-vs12")
win_x86_vs12.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs12_env))
win_x86_vs12.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs12_env))
win_x86_vs12.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs12_env)
win_x86_vs12.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs12_env)
#win_x86_vs12.add_linkflag('/subsystem:console')


win_x64_vs12 = pybuild.CXXToolchain("windows-x64-pybuild-vs12")
win_x64_vs12.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs12_env))
win_x64_vs12.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs12_env))
win_x64_vs12.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs12_env)
win_x64_vs12.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs12_env)
#win_x64_vs12.add_linkflag('/subsystem:console')


win_x86_vs14_clang = pybuild.CXXToolchain("windows-x86-pybuild-clang-vs14")
win_x86_vs14_clang.add_tool('.S', clang.PyBuildCXXCompiler(cxx=False))
win_x86_vs14_clang.add_tool('.c', clang.PyBuildCXXCompiler(cxx=False))
win_x86_vs14_clang.add_tool('.cc', clang.PyBuildCXXCompiler(cxx=True))
win_x86_vs14_clang.add_tool('.cpp', clang.PyBuildCXXCompiler(cxx=True))
win_x86_vs14_clang.add_tool('.cxx', clang.PyBuildCXXCompiler(cxx=True))
win_x86_vs14_clang.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs14_env)
win_x86_vs14_clang.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs14_env)
win_x86_vs14_clang.add_cflag('-m32')
win_x86_vs14_clang.add_cxxflag('-m32')
win_x86_vs14_clang.add_linkflag('/defaultlib:msvcrt')
win_x86_vs14_clang.add_linkflag('/defaultlib:oldnames')


win_x64_vs14_clang = pybuild.CXXToolchain("windows-x64-pybuild-clang-vs14")
win_x64_vs14_clang.add_tool('.S', clang.PyBuildCXXCompiler(cxx=False))
win_x64_vs14_clang.add_tool('.c', clang.PyBuildCXXCompiler(cxx=False))
win_x64_vs14_clang.add_tool('.cc', clang.PyBuildCXXCompiler(cxx=True))
win_x64_vs14_clang.add_tool('.cpp', clang.PyBuildCXXCompiler(cxx=True))
win_x64_vs14_clang.add_tool('.cxx', clang.PyBuildCXXCompiler(cxx=True))
win_x64_vs14_clang.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs14_env)
win_x64_vs14_clang.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs14_env)
win_x64_vs14_clang.add_cflag('-m64')
win_x64_vs14_clang.add_cxxflag('-m64')
win_x64_vs14_clang.add_linkflag('/defaultlib:msvcrt')
win_x64_vs14_clang.add_linkflag('/defaultlib:oldnames')
