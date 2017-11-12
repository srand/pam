##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


from build.transform import utils
import pybuild
import os

class CXXProject(pybuild.CXXProject):
    def __init__(self, toolchain, name, vcvars):
        super(CXXProject).__init__(toolchain, name)
        self.vcvars

    def transform(self):
        rc, _ = utils.execute('nmake.exe /nologo {}.nmake '.format(self.name), self.vcvars)
        if rc != 0:
            raise RuntimeError()
        return True


class CXXToolchain(pybuild.CXXToolchain):
    def __init__(self, name, vcvars):
        super(CXXToolchain, self).__init__(name)
        self.vcvars = vcvars
        
    def generate(self, project, toolchain):
        cxx_project = super(CXXToolchain, self).generate(project)
        with open('{}.nmake'.format(project.name), 'w') as f:
            f.write('all: {}\n\n'.format(cxx_project.job.product))
            for cmd in cxx_project.commands:
                f.write('{product}: {deps}\n'.format(product=cmd.product, deps=' '.join(cmd.dependencies())))
                f.write('\t@echo {info}\n'.format(info=cmd.info))
                f.write('\t@{cmdline}\n'.format(cmdline=cmd.cmdline))
                f.write('\n')
        return CXXProject(toolchain, project.name)
        
        
    def transform(self, project, toolchain):
        return self.generate(project, toolchain).transform()
        
