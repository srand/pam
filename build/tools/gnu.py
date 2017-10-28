##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


from build.tools import Tool
from build.tools.directory import PyBuildDirectoryCreator
from build.transform import pybuild
from os import path


class PyBuildCXXCompiler(Tool):
    def __init__(self, cxx=False):
        self._executable = 'gcc' if not cxx else 'g++'
        self._cxx = cxx
        self._output_ext = '.o'

    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)

    def _product(self, cxx_project, source_file):
        return '{output}/{}{}'.format(source_file, self._output_ext, output=cxx_project.output)

    def _cmdline(self, cxx_project, source_file):
        incpaths = ['-I{}'.format(path) for path in cxx_project.incpaths]
        flags = cxx_project.cflags if not self._cxx else cxx_project.cxxflags

        return "{} -x {} {} -c {} -o {}".format(
            self._executable,
            'c++' if self._cxx else 'c', 
            ' '.join(flags),
            source_file, 
            self._product(cxx_project, source_file))

    def _info(self, source_file):
        return ' [{}] {}'.format(self._executable.upper(), source_file)

    def transform(self, cxx_project, source_file):
        product = self._product(cxx_project, source_file.path)
        dir = self._directory(cxx_project, path.dirname(product))
        obj =  pybuild.Object(
            product, 
            self._cmdline(cxx_project, source_file.path), 
            self._info(source_file.path))
        cxx_project.add_job(pybuild.Source(source_file.path))
        cxx_project.add_job(obj)
        cxx_project.add_dependency(obj.product, source_file.path)
        cxx_project.add_dependency(obj.product, dir.product)
        return obj


class PyBuildCXXArchiver(Tool):
    def __init__(self):
        self._executable = 'ar'
        self._output_pfx = 'lib'
        self._output_ext = '.a'

    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)
        
    def _product(self, cxx_project):
        return '{output}/{}{}{}'.format(self._output_pfx, cxx_project.name, self._output_ext, output=cxx_project.output)

    def _cmdline(self, cxx_project, object_files):
        return "{} cr {} {}".format(self._executable, self._product(cxx_project), ' '.join(object_files))

    def _info(self, cxx_project):
        return ' [{}] {}'.format(self._executable.upper(), cxx_project.name)

    def transform(self, project, cxx_project, object_files):
        product = self._product(cxx_project)
        dir = self._directory(cxx_project, path.dirname(product))
        library = pybuild.Object(
            product, 
            self._cmdline(cxx_project, object_files), 
            self._info(cxx_project))
        cxx_project.add_job(library)
        cxx_project.add_dependency(library.product, dir.product)
        for obj in object_files:
            cxx_project.add_dependency(library.product, obj)
        return library


class PyBuildCXXLinker(Tool):
    def __init__(self, cxx=False, executable='g++'):
        self._executable = executable
        self._cxx = cxx
        self._output_ext = ''

    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)
        
    def _product(self, cxx_project):
        return '{output}/{}{}'.format(cxx_project.name, self._output_ext, output=cxx_project.output)

    def _cmdline(self, project, cxx_project, object_files):
        libpaths = ['-L{}'.format(path) for path in cxx_project.libpaths]
        libpaths += ['-L{output}/{lib}'.format(output=cxx_project.toolchain.attributes.output, lib=lib) for lib in cxx_project.libraries]
        libraries = ['-l{}'.format(path) for path in cxx_project.libraries]
        flags = cxx_project.linkflags

        return "{} {} {} -o {} {} -Wl,--start-group {} -Wl,--end-group".format(
            self._executable, 
            ' '.join(flags),
            ' '.join(object_files),
            self._product(cxx_project),
            ' '.join(libpaths),
            ' '.join(libraries))

    def _info(self, cxx_project):
        return ' [{}] {}'.format(self._executable.upper(), cxx_project.name)

    def transform(self, project, cxx_project, object_files):
        product = self._product(cxx_project)
        dir = self._directory(cxx_project, path.dirname(product))
        executable = pybuild.Object(
            product, 
            self._cmdline(project, cxx_project, object_files), 
            self._info(cxx_project))
        cxx_project.add_job(executable)                            
        cxx_project.add_dependency(executable.product, dir.product)
        for obj in object_files:
            cxx_project.add_dependency(executable.product, obj)
        return executable
