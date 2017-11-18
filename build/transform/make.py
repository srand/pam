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
from build.utils import Dispatch, multidispatch
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
        return True


class CXXToolchain(pybuild.CXXToolchain):
    dispatch = Dispatch()

    def __init__(self, name):
        super(CXXToolchain, self).__init__(name)

    @staticmethod
    def _regular_deps(job):
        return [dep for dep in job.dependencies() 
                if not isinstance(job.get_dependency(dep), Directory)
                and not isinstance(job.get_dependency(dep), pybuild.FileList)] 

    @staticmethod
    def _rebuild_deps(job):
        return [dep for dep in job.dependencies() 
                if isinstance(job.get_dependency(dep), Directory)
                or isinstance(job.get_dependency(dep), pybuild.FileList)] 

    @staticmethod
    def _visit_cmd(job, f):
        f.write('{product}: {regular_deps} | {rebuild_deps}\n'.format(
            product=job.product,
            regular_deps=" ".join(CXXToolchain._regular_deps(job)),
            rebuild_deps=" ".join(CXXToolchain._rebuild_deps(job))))
        f.write('\t@echo {info}\n'.format(info=job.info))
        f.write('\t@{cmdline}\n'.format(cmdline=job.cmdline))
        f.write('\n')

    @multidispatch(dispatch, pybuild.Command, file)
    def _visit(job, f):
        CXXToolchain._visit_cmd(job, f)

    @multidispatch(dispatch, pybuild.Object, file)
    def _visit(job, f):
        CXXToolchain._visit_cmd(job, f)
        depfile,_ = os.path.splitext(job.product)
        f.write("-include {depfile}.d\n".format(depfile=depfile))
        f.write("\n")

    @multidispatch(dispatch, Directory, file)
    def _visit(job, f):
        CXXToolchain._visit_cmd(job, f)

    @multidispatch(dispatch, pybuild.FileList, file)
    def _visit(job, f):
        f.write('{product}:\n'.format(product=job.product))
        f.write('\t@echo {info}\n'.format(info=job.info))
        f.write('\t@rm -f {product}\n'.format(product=job.product))
        for file in job.files:
            f.write('\t@echo {file} >> {product}\n'.format(file=file, product=job.product))
        f.write('\n')

    @multidispatch(dispatch)
    def _visit(job, f):
        pass

    def generate(self, project, toolchain=None):
        toolchain = toolchain if toolchain else self
        cxx_project = super(CXXToolchain, self).generate(project, toolchain)
        with open('{}.mk'.format(project.name), 'w') as f:
            f.write('.PHONY: all\n')
            f.write('all: {}\n\n'.format(cxx_project.job.product))
            for job in cxx_project.jobs:
                self._visit(job, f)
            
        return CXXProject(toolchain, project.name)
        
        
    def transform(self, project):
        return self.generate(project, self).transform()
