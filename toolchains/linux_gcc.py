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

gcc_mk = MakeCXXToolchain("make-gcc")
tools.configure(gcc_mk)
features.configure(gcc_mk)

linux_mk = ToolchainExtender("linux-make-gcc", gcc_mk)
linux_mk.add_requirement(HostRequirement.LINUX)
