from build.transform import msbuild 
from build.transform import pybuild
from build.transform import nmake
from build.feature import Feature
from build.tools import msvc, clang
from build.transform.visual_studio import VS12VCVars, VS14VCVars


_win_x86_vs12_env = VS12VCVars(host="x64", target="x86")
_win_x64_vs12_env = VS12VCVars(host="x64", target="x64")
_win_x86_vs14_env = VS14VCVars(host="x64", target="x86")
_win_x64_vs14_env = VS14VCVars(host="x64", target="x64")


def PlatformToolset(platform='Win32', toolset='v140', charset='MultiByte'):
    class _PlatformToolset:
        def transform(self, project, cxx_project):
            cxx_project.globals_group.platform = platform
            cxx_project.config_props.toolset = toolset
            cxx_project.config_props.charset = charset
    return _PlatformToolset()


win_x86_vs12_msbuild = msbuild.CXXToolchain("windows-x86-msbuild-vs12", _win_x86_vs12_env)
win_x86_vs12_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x86_vs12_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs12_msbuild.add_feature(PlatformToolset(toolset='v120_xp'))


win_x64_vs12_msbuild = msbuild.CXXToolchain("windows-x64-msbuild-vs12", _win_x86_vs12_env)
win_x64_vs12_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x64_vs12_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs12_msbuild.add_feature(PlatformToolset(platform='x64', toolset='v120_xp'))


win_x86_vs14_msbuild = msbuild.CXXToolchain("windows-x86-msbuild-vs14", _win_x86_vs14_env)
win_x86_vs14_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x86_vs14_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs14_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs14_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x86_vs14_msbuild.add_feature(PlatformToolset(toolset='v140_xp'))


win_x64_vs14_msbuild = msbuild.CXXToolchain("windows-x64-msbuild-vs14", _win_x86_vs14_env)
win_x64_vs14_msbuild.add_tool('.c', msvc.MSBuildCXXCompiler(cxx=False))
win_x64_vs14_msbuild.add_tool('.cc', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs14_msbuild.add_tool('.cpp', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs14_msbuild.add_tool('.cxx', msvc.MSBuildCXXCompiler(cxx=True))
win_x64_vs14_msbuild.add_feature(PlatformToolset(platform='x64', toolset='v140_xp'))


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


win_x86_vs14 = pybuild.CXXToolchain("windows-x86-pybuild-vs14")
win_x86_vs14.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs14_env)
win_x86_vs14.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs14_env)
#win_x86_vs14.add_linkflag('/subsystem:console')


win_x64_vs14 = pybuild.CXXToolchain("windows-x64-pybuild-vs14")
win_x64_vs14.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs14_env)
win_x64_vs14.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs14_env)
#win_x64_vs14.add_linkflag('/subsystem:console')


win_x86_vs14_nmake = nmake.CXXToolchain("windows-x86-nmake-vs14", _win_x86_vs14_env)
win_x86_vs14_nmake.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs14_env))
win_x86_vs14_nmake.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x86_vs14_env))
win_x86_vs14_nmake.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14_nmake.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14_nmake.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x86_vs14_env))
win_x86_vs14_nmake.archiver = msvc.PyBuildCXXArchiver(env=_win_x86_vs14_env)
win_x86_vs14_nmake.linker = msvc.PyBuildCXXLinker(env=_win_x86_vs14_env)
#win_x86_vs14_nmake.add_linkflag('/subsystem:console')


win_x64_vs14_nmake = nmake.CXXToolchain("windows-x64-nmake-vs14", _win_x64_vs14_env)
win_x64_vs14_nmake.add_tool('.S', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs14_env))
win_x64_vs14_nmake.add_tool('.c', msvc.PyBuildCXXCompiler(cxx=False, env=_win_x64_vs14_env))
win_x64_vs14_nmake.add_tool('.cc', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14_nmake.add_tool('.cpp', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14_nmake.add_tool('.cxx', msvc.PyBuildCXXCompiler(cxx=True, env=_win_x64_vs14_env))
win_x64_vs14_nmake.archiver = msvc.PyBuildCXXArchiver(env=_win_x64_vs14_env)
win_x64_vs14_nmake.linker = msvc.PyBuildCXXLinker(env=_win_x64_vs14_env)
#win_x64_vs14.add_linkflag('/subsystem:console')


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
