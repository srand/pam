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
from build.utils import DepfileParser
from os import path, pathsep, environ
from copy import copy
from functools import partial


class _ExecutableMixin(object):
    def __init__(self, executable, filetype=None, prefix=None, path=None, *args, **kwargs):
        super(_ExecutableMixin, self).__init__(*args, **kwargs)
        self.prefix = prefix or ''
        self.bare_executable = executable
        self.executable = self.prefix + self.bare_executable
        self.filetype = filetype
        self.path = path or ''
        self.environ = copy(environ)
        if self.path and self.environ["PATH"]:
            self.environ["PATH"] += pathsep + path 


def _scan_deps(cxx_project, obj):
    depfile, _ = path.splitext(obj.product)
    obj.clear_hash()
    for dep in DepfileParser(depfile + ".d").dependencies:
        cxx_project.add_source(dep)
        cxx_project.add_dependency(obj.product, dep)


class PyBuildCXXCompiler(_ExecutableMixin, Tool):
    def __init__(self, executable='g++', filetype='c++', *args, **kwargs):
        super(PyBuildCXXCompiler, self).__init__(executable=executable, filetype=filetype, *args, **kwargs)
        self._output_ext = '.o'

    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)

    def _product(self, cxx_project, source_file):
        return '{output}/{}{}'.format(source_file, self._output_ext, output=cxx_project.output)

    def _cmdline(self, cxx_project, source_file):
        flags = cxx_project.cflags if self.filetype != 'c++' else cxx_project.cxxflags

        return "{} -x {} {} -MMD -c {} -o {}".format(
            self.executable,
            self.filetype, 
            ' '.join(flags),
            source_file, 
            self._product(cxx_project, source_file))

    def _info(self, source_file):
        return ' [{}] {}'.format(self.bare_executable.upper(), source_file)

    def transform(self, cxx_project, source_file):
        product = self._product(cxx_project, source_file.path)
        dir = self._directory(cxx_project, path.dirname(product))
        obj =  pybuild.Object(
            product, 
            self._cmdline(cxx_project, source_file.path), 
            self._info(source_file.path),
            self.environ)
        cxx_project.add_source(source_file.path)
        cxx_project.add_job(obj)
        cxx_project.add_dependency(obj.product, source_file.path)
        cxx_project.add_dependency(obj.product, dir.product)

        obj.on_completed = partial(_scan_deps, cxx_project)
        obj.on_completed(obj)

        return obj


class PyBuildCXXArchiver(_ExecutableMixin, Tool):
    def __init__(self, executable='ar', *args, **kwargs):
        super(PyBuildCXXArchiver, self).__init__(executable=executable, *args, **kwargs)
        self._output_pfx = 'lib'
        self._output_ext = '.a'

    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)
        
    def _product(self, cxx_project):
        return '{output}/{}{}{}'.format(self._output_pfx, cxx_project.name, self._output_ext, output=cxx_project.output)

    def _filelist(self, cxx_project):
        return self._product(cxx_project) + ".objects"

    def _cmdline(self, cxx_project, object_files):
        return "{} cr {} @{}".format(self.executable, self._product(cxx_project), self._filelist(cxx_project))

    def _info(self, cxx_project):
        return ' [{}] {}'.format(self.bare_executable.upper(), cxx_project.name)

    def transform(self, project, cxx_project, object_files):
        product = self._product(cxx_project)
        dir = self._directory(cxx_project, path.dirname(product))
        library = pybuild.Object(
            product, 
            self._cmdline(cxx_project, object_files), 
            self._info(cxx_project),
            self.environ)
        filelist = cxx_project.add_filelist(self._filelist(cxx_project), object_files)
        cxx_project.add_job(library)
        cxx_project.add_dependency(library.product, dir.product)
        cxx_project.add_dependency(library.product, filelist.product)
        cxx_project.add_dependency(filelist.product, dir.product)
        for obj in object_files:
            cxx_project.add_dependency(library.product, obj)

        library.on_completed = partial(_scan_deps, cxx_project)
        library.on_completed(library)

        return library


class PyBuildCXXLinker(_ExecutableMixin, Tool):
    def __init__(self, executable='g++', *args, **kwargs):
        super(PyBuildCXXLinker, self).__init__(executable=executable, *args, **kwargs)
        self._output_ext = ''

    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)
        
    def _product(self, cxx_project):
        return '{output}/{}{}'.format(cxx_project.name, self._output_ext, output=cxx_project.output)

    def _filelist(self, cxx_project):
        return self._product(cxx_project) + ".objects"

    def _cmdline(self, project, cxx_project, object_files):
        libpaths = ['-L{output}/{lib}'.format(output=cxx_project.toolchain.attributes.output, lib=lib) for lib in cxx_project.libraries]
        libraries = ['-l{}'.format(path) for path in cxx_project.libraries]
        flags = cxx_project.linkflags

        return "{} {} @{} -o {} {} -Wl,--start-group {} -Wl,--end-group".format(
            self.executable, 
            ' '.join(flags),
            self._filelist(cxx_project),
            self._product(cxx_project),
            ' '.join(libpaths),
            ' '.join(libraries))

    def _info(self, cxx_project):
        return ' [{}] {}'.format(self.bare_executable.upper(), cxx_project.name)

    def transform(self, project, cxx_project, object_files):
        product = self._product(cxx_project)
        dir = self._directory(cxx_project, path.dirname(product))
        executable = pybuild.Object(
            product, 
            self._cmdline(project, cxx_project, object_files), 
            self._info(cxx_project),
            self.environ)
        filelist = cxx_project.add_filelist(self._filelist(cxx_project), object_files)
        cxx_project.add_job(executable)
        cxx_project.add_dependency(executable.product, dir.product)
        cxx_project.add_dependency(executable.product, filelist.product)
        cxx_project.add_dependency(filelist.product, dir.product)
        for obj in object_files:
            cxx_project.add_dependency(executable.product, obj)

        executable.on_completed = partial(_scan_deps, cxx_project)
        executable.on_completed(executable)

        return executable


class GNUToolFactory:
    def __init__(self, prefix=None, path=None):
        self.prefix = prefix
        self.path = path

    def configure(self, toolchain):
        toolchain.add_tool('.s', PyBuildCXXCompiler('gcc', 'assembler', prefix=self.prefix, path=self.path))
        toolchain.add_tool('.S', PyBuildCXXCompiler('gcc', 'assembler-with-cpp', prefix=self.prefix, path=self.path))
        toolchain.add_tool('.c', PyBuildCXXCompiler('gcc', 'c', prefix=self.prefix, path=self.path))
        toolchain.add_tool('.cc', PyBuildCXXCompiler('g++', 'c++', prefix=self.prefix, path=self.path))
        toolchain.add_tool('.cpp', PyBuildCXXCompiler('g++', 'c++', prefix=self.prefix, path=self.path))
        toolchain.add_tool('.cxx', PyBuildCXXCompiler('g++', 'c++', prefix=self.prefix, path=self.path))
        toolchain.archiver = PyBuildCXXArchiver(prefix=self.prefix, path=self.path)
        toolchain.linker = PyBuildCXXLinker(prefix=self.prefix, path=self.path)
