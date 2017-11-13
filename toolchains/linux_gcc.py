from build.transform.pybuild import CXXToolchain as PamCXXToolchain
from build.transform.make import CXXToolchain as MakeCXXToolchain
from build.transform.toolchain import ToolchainExtender
from build.tools.gnu import GNUToolFactory
from build.features.pybuild import *
from build.requirement import HostRequirement 


tools = GNUToolFactory()
features = GNUFeatureFactory()

gcc = PamCXXToolchain("pam-gcc")
tools.configure(gcc)
features.configure(gcc)

linux = ToolchainExtender("linux-pam-gcc", gcc)
linux.add_requirement(HostRequirement.LINUX)

linux_x86 = ToolchainExtender("linux-x86-pam-gcc", linux)
linux_x86.add_feature(PyBuildCustomCFlag('-m32'))
linux_x86.add_feature(PyBuildCustomCXXFlag('-m32'))
linux_x86.add_feature(PyBuildCustomLinkerFlag('-m32'))

linux_x64 = ToolchainExtender("linux-x64-pam-gcc", linux)
linux_x86.add_feature(PyBuildCustomCFlag('-m64'))
linux_x86.add_feature(PyBuildCustomCXXFlag('-m64'))
linux_x86.add_feature(PyBuildCustomLinkerFlag('-m64'))


gcc_mk = MakeCXXToolchain("make-gcc")
tools.configure(gcc_mk)
features.configure(gcc_mk)

linux_mk = ToolchainExtender("linux-make-gcc", gcc_mk)
linux_mk.add_requirement(HostRequirement.LINUX)

linux_x86_mk = ToolchainExtender("linux-x86-make-gcc", linux_mk)
linux_x86_mk.add_feature(PyBuildCustomCFlag('-m32'))
linux_x86_mk.add_feature(PyBuildCustomCXXFlag('-m32'))
linux_x86_mk.add_feature(PyBuildCustomLinkerFlag('-m32'))

linux_x64_mk = ToolchainExtender("linux-x64-make-gcc", linux_mk)
linux_x86_mk.add_feature(PyBuildCustomCFlag('-m64'))
linux_x86_mk.add_feature(PyBuildCustomCXXFlag('-m64'))
linux_x86_mk.add_feature(PyBuildCustomLinkerFlag('-m64'))
