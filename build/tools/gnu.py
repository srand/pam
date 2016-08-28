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
        def key_value(key, value):
            return "{}".format(key) if value is None else "{}={}".format(key, value)
		
        definitions = ['-D{}'.format(key_value(key, value)) for key, value in cxx_project.macros ]
        incpaths = ['-I{}'.format(path) for path in cxx_project.incpaths]
        flags = cxx_project.cflags if not self._cxx else cxx_project.cxxflags

        return "{} -x {} {} {} {} -c {} -o {}".format(
            self._executable,
            'c++' if self._cxx else 'c', 
            ' '.join(flags),
            ' '.join(definitions),
            ' '.join(incpaths),
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

    def transform(self, cxx_project, object_files):
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


class PyBuildCXXLinker(Tool):
    def __init__(self, cxx=False, executable='gcc'):
        self._executable = executable
        self._cxx = cxx
        self._output_ext = ''

    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)
        
    def _product(self, cxx_project):
        return '{output}/{}{}'.format(cxx_project.name, self._output_ext, output=cxx_project.output)

    def _cmdline(self, cxx_project, object_files):
        libpaths = ['-L{}'.format(path) for path in cxx_project.libpaths]
        libpaths += ['-L{output}/{lib}'.format(output=cxx_project.toolchain.attributes.output, lib=lib) for lib in cxx_project.libraries]
        libraries = ['-l{}'.format(path) for path in cxx_project.libraries]
        flags = cxx_project.linkflags

        return "{} {} {} -o {} {} {}".format(
            self._executable, 
            ' '.join(flags),
            ' '.join(object_files),
            self._product(cxx_project),
            ' '.join(libpaths),
            ' '.join(libraries))

    def _info(self, cxx_project):
        return ' [{}] {}'.format(self._executable.upper(), cxx_project.name)

    def transform(self, cxx_project, object_files):
        product = self._product(cxx_project)
        dir = self._directory(cxx_project, path.dirname(product))
        executable = pybuild.Object(
            product, 
            self._cmdline(cxx_project, object_files), 
            self._info(cxx_project))
        cxx_project.add_job(executable)                            
        cxx_project.add_dependency(executable.product, dir.product)
        for obj in object_files:
            cxx_project.add_dependency(executable.product, obj)
