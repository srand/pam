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
from build.transform import msbuild 
from build.transform import pybuild
from os import path


class MSBuildCSCompiler(Tool):
    def transform(self, msproject, sources):
        ig = msproject.create_item_group()
        for source in sources:
            ig.create_compile(source.path)
        return ig


class MSBuildCXXCompiler(Tool):
    def __init__(self, cxx=True):
        self.cxx = cxx
        
    def transform(self, cxx_project, sources):
        ig = cxx_project.create_item_group()
        for source in sources:
            cl = ig.create_clcompile(source.path)
            if not self.cxx:
                cl.compileas = "CompileAsC"
                cl.compileaswinrt = "false"
        return ig


class MSBuildShaderCompiler(Tool):
    def transform(self, msproject, sources):
        ig = msproject.create_item_group()
        for source in sources:
            fx = ig.create_fxcompile(source.path)
            fx.shadertype = source.args['shadertype'].title()
            fx.shadermodel = source.args['shadermodel']
        return ig


class MSBuildImage(Tool):
    def transform(self, msproject, sources):
        ig = msproject.create_item_group()
        for source in sources:
            img = ig.create_image(source.path)
        return ig


class MSBuildMedia(Tool):
    def transform(self, msproject, sources):
        ig = msproject.create_item_group()
        for source in sources:
            img = ig.create_media(source.path)
        return ig


class MSBuildNoneTask(Tool):
    def transform(self, msproject, sources):
        ig = msproject.create_item_group()
        for source in sources:
            img = ig.create_nonetask(source.path)
        return ig


class MSBuildContent(Tool):
    def transform(self, msproject, sources):
        ig = msproject.create_item_group()
        for source in sources:
            img = ig.create_content(source.path)
        return ig


class MSBuildAppxManifest(Tool):
    def transform(self, msproject, sources):
        ig = msproject.create_item_group()
        for source in sources:
            appx = ig.create_appxmanifest(source.path)
        return ig


class PyBuildCXXCompiler(Tool):
    def __init__(self, cxx=False, env=None):
        self._executable = "cl.exe"
        self._output_ext = ".obj"
        self._cxx = cxx
        self._env = env
        
    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)
        
    def _product(self, cxx_project, source_file):
        return path.join(cxx_project.output, '{}{}'.format(source_file, self._output_ext))
        
    def _cmdline(self, cxx_project, source_file):
        def key_value(key, value):
            return "{}".format(key) if value is None else "{}={}".format(key, value)
		
        definitions = ['/D{}'.format(key_value(key, value)) for key, value in cxx_project.macros ]
        incpaths = ['/I{}'.format(path) for path in cxx_project.incpaths]
        flags = cxx_project.cflags if not self._cxx else cxx_project.cxxflags

        return "{} /nologo {} {} {} /c /T{}{} /Fo{} > nul".format(
            self._executable, 
            ' '.join(flags),
            ' '.join(definitions),
            ' '.join(incpaths),
            'p' if self._cxx else 'c',
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
            self._info(source_file.path),
            self._env)
        cxx_project.add_job(pybuild.Source(source_file.path))
        cxx_project.add_job(obj)
        cxx_project.add_dependency(obj.product, source_file.path)
        cxx_project.add_dependency(obj.product, dir.product)
        return obj


class PyBuildCXXArchiver(Tool):
    def __init__(self, env=None):
        self._executable = 'lib.exe'
        self._output_pfx = ''
        self._output_ext = '.lib'
        self._env = env

    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)

    def _product(self, cxx_project):
        return path.join(cxx_project.output, '{}{}{}'.format(self._output_pfx, cxx_project.name, self._output_ext))

    def _cmdline(self, cxx_project, object_files):
        return "{} /nologo /out:{} {}".format(
            self._executable,
            self._product(cxx_project), 
            ' '.join(object_files))

    def _info(self, cxx_project):
        return ' [{}] {}'.format(self._executable.upper(), cxx_project.name)

    def transform(self, project, cxx_project, object_files):
        product = self._product(cxx_project)
        dir = self._directory(cxx_project, path.dirname(product))
        library = pybuild.Object(
            product, 
            self._cmdline(cxx_project, object_files), 
            self._info(cxx_project),
            self._env)
        cxx_project.add_job(library)
        cxx_project.add_dependency(library.product, dir.product)
        for obj in object_files:
            cxx_project.add_dependency(library.product, obj)
        return library


class PyBuildCXXLinker(Tool):
    def __init__(self, env=None):
        self._executable = 'link.exe'
        self._output_ext = '.exe'
        self._output_ext_dll = '.dll'
        self._env = env

    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)

    def _product(self, project, cxx_project):
        return path.join(cxx_project.output, '{}{}'.format(
            cxx_project.name, self._output_ext_dll if project.shared else self._output_ext))

    def _cmdline(self, project, cxx_project, object_files):
        libpaths = ['/libpath:{}'.format(path) for path in cxx_project.libpaths]
        libraries = ['{output}/{lib}/{lib}.lib'.format(output=cxx_project.toolchain.attributes.output, lib=lib) for lib in cxx_project.libraries]
        flags = cxx_project.linkflags

        return "{} /nologo {} {} {} {} {} /out:{}".format(
            self._executable, 
            '/dll' if project.shared else '',
            ' '.join(libpaths),
            ' '.join(libraries),
            ' '.join(flags),
            ' '.join(object_files),
            self._product(project, cxx_project))

    def _info(self, cxx_project):
        return ' [{}] {}'.format(self._executable.upper(), cxx_project.name)

    def transform(self, project, cxx_project, object_files):
        product = self._product(project, cxx_project)
        dir = self._directory(cxx_project, path.dirname(product))
        executable = pybuild.Object(
            product, 
            self._cmdline(project, cxx_project, object_files), 
            self._info(cxx_project),
            self._env)
        cxx_project.add_job(executable)                            
        cxx_project.add_dependency(executable.product, dir.product)
        for obj in object_files:
            cxx_project.add_dependency(executable.product, obj)
        return executable

