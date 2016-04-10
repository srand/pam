from build.transform.native import GNUCXXToolchain 

linux_x86 = GNUCXXToolchain("linux-x86-gcc")
linux_x86.add_cflag('-m32')
linux_x86.add_cxxflag('-m32')
linux_x86.add_linkflag('-m32')

linux_x64 = GNUCXXToolchain("linux-x64-gcc")
linux_x64.add_cflag('-m64')
linux_x64.add_cxxflag('-m64')
linux_x64.add_linkflag('-m64')

