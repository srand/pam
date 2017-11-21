from build.transform.pybuild import CXXToolchain
from build.transform.toolchain import ToolchainExtender
from build.tools import clang
from build.features.pybuild import *
from build.requirement import HostRequirement

tools = clang.ClangToolFactory()
features = GNUFeatureFactory()

macosx = CXXToolchain("macosx-pam-clang")
tools.configure(macosx)
features.configure(macosx)
macosx.add_requirement(HostRequirement.DARWIN)
macosx.add_feature(PyBuildCustomCFlag.C89, 'language-c89')
macosx.add_feature(PyBuildCustomCFlag.C99, 'language-c99')
macosx.add_feature(PyBuildCustomCFlag.C11, 'language-c11')
macosx.add_feature(PyBuildCustomCXXFlag.CXX11, 'language-c++11')
macosx.add_feature(PyBuildCustomCXXFlag.CXX14, 'language-c++14')
macosx.add_feature(PyBuildCustomCXXFlag.CXX17, 'language-c++17')
macosx.add_feature(PyBuildOptimize.GNU, 'optimize')
macosx.add_feature(PyBuildProjectMacros.GNU)
macosx.add_feature(PyBuildProjectIncPaths.GNU)
macosx.add_feature(PyBuildProjectLibPaths.GNU)
macosx.add_feature(PyBuildProjectDeps.GNU)
