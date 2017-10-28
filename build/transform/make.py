##############################################################################
#
# (C) 2017 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


from build.transform import utils
from build.tools.directory import Directory
import pybuild
import os
import multiprocessing


class CXXProject(pybuild.CXXProject):
    def __init__(self, toolchain, name):
        super(CXXProject, self).__init__(toolchain, name)

    def transform(self):
        rc, _, _ = utils.execute('make -f {}.mk -j {} all'.format(
            self.name, multiprocessing.cpu_count()))
        if rc != 0:
            raise RuntimeError(rc)


class CXXToolchain(pybuild.CXXToolchain):
    def __init__(self, name):
        super(CXXToolchain, self).__init__(name)
        
    def generate(self, project, toolchain=None):
        toolchain = toolchain if toolchain else self
        cxx_project = super(CXXToolchain, self).generate(project, toolchain)
        with open('{}.mk'.format(project.name), 'w') as f:
            f.write('.PHONY: all\n')
            f.write('all: {}\n\n'.format(cxx_project.job.product))
            for cmd in cxx_project.commands:
                deps = cmd.dependencies()
                deps = [dep for dep in deps if not isinstance(cmd.get_dependency(dep), Directory)] 
                dir_deps = cmd.dependencies()
                dir_deps = [dep for dep in dir_deps if isinstance(cmd.get_dependency(dep), Directory)] 
                f.write('{product}: {deps} | {dir_deps}\n'.format(
                    product=cmd.product,
                    deps=' '.join(deps),
                    dir_deps=' '.join(dir_deps)))
                f.write('\t@echo {info}\n'.format(info=cmd.info))
                f.write('\t@{cmdline}\n'.format(cmdline=cmd.cmdline))
                f.write('\n')
        return CXXProject(toolchain, project.name)
        
        
    def transform(self, project):
        self.generate(project, self).transform()
        
