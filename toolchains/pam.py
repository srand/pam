from build.tools import gnu, msvc
import build.features.pybuild as pybuild
from build.transform.toolchain import *
import build.transform.pybuild as pybuildtc


def pam_gnu_toolchain(
    name,
    inherits=None,
    cflags=None,
    cxxflags=None,
    linkflags=None,
    prefix=None,
    path=None,
    sysroot=None,
):
    if inherits:
        tc = ToolchainRegistry.find(inherits)
    else:
        tc = pybuildtc.CXXToolchain(name)
        gnu.GNUToolFactory(prefix=prefix, path=path).configure(tc)
        pybuild.GNUFeatureFactory().configure(tc)

    tc = ToolchainExtender(name, tc)
    if cflags:
        tc.add_feature(pybuild.PyBuildCustomCFlag(cflags))
    if cxxflags:
        tc.add_feature(pybuild.PyBuildCustomCXXFlag(cxxflags))
    if linkflags:
        tc.add_feature(pybuild.PyBuildCustomLinkerFlag(linkflags))
    if sysroot:
        sysroot = "--sysroot={}".format(sysroot)
        tc.add_feature(pybuild.PyBuildCustomCFlag(sysroot))
        tc.add_feature(pybuild.PyBuildCustomCXXFlag(sysroot))
        tc.add_feature(pybuild.PyBuildCustomLinkerFlag(sysroot))
    return tc


def pam_msvc_toolchain(
    name,
    inherits,
    cflags=None,
    cxxflags=None,
    linkflags=None,
):
    tc = ToolchainRegistry.find(inherits)
    tc = ToolchainExtender(name, tc)
    if cflags:
        tc.add_feature(pybuild.PyBuildCustomCFlag(cflags))
    if cxxflags:
        tc.add_feature(pybuild.PyBuildCustomCXXFlag(cxxflags))
    if linkflags:
        tc.add_feature(pybuild.PyBuildCustomLinkerFlag(linkflags))
    return tc
