##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


from build.utils import Loader
from build.transform import utils
import os
import re
import uuid


class _Filtered(object):
    def __init__(self, filter):
        super(_Filtered, self).__init__()
        self.filter = filter
        
    def matches(self, toolchain):
        if self.filter is None:
            return True
        return re.search(self.filter, toolchain) is not None


class _FilteredAndPublished(_Filtered):
    def __init__(self, filter, publish):
        super(_FilteredAndPublished, self).__init__(filter)
        self.publish = publish


class ToolchainGroup(object):
    """ A collection of toolchain identifiers """

    def __init__(self):
        super(ToolchainGroup, self).__init__()
        self.toolchains = []

    def add_toolchain(self, toolchain):
        """ Adds a toolchain identifier (string) to the collection """
        self.toolchains.append(toolchain)


class Source(_Filtered):
    """ Representation of a project source file """

    def __init__(self, path, filter=None, tool=None, args=None):
        super(Source, self).__init__(filter)
        self.path = os.path.normpath(path)
        self.args = args
        _, self.tool = (None, tool) if tool is not None else os.path.splitext(self.path)

    @property
    def sources(self):
        return [self]


class SourceGroup(object):
    """ A collection of source files.

        A source group can be reused in multiple projects. 
    
        Some toolchains can use source groups to organize sources logically.
        For example, MSBuild toolchains tranform source groups into filters 
        which are visible as folders if the generated project is loaded in 
        Visual Studio. The filter's name will be **name** if provided.
    """

    def __init__(self, name=None):
        super(SourceGroup, self).__init__()
        self._sources = []
        self.name = name

    def add_sources(self, path, regex=r'.*', recurse=False, filter=None, tool=None, files=None, **kwargs):
        """ Add sources from **path** to the group. Directories will be enumerated, 
        but child directories won't unless **recurse** is True. **regex** can be used
        to filter the resulting list of files. 
        
        File extensions are used to find a matching tool to be associated with the source file. 
        If an unconventional file extension is used, a tool can be explicitly selected by 
        providing the extension, such as '.cpp' in the **tool** argument.

        The **filter** regex makes it possible to add sources conditionally for a
        specific toolchain. The regex is matched against the toolchain
        identifier to determine if the sources should be built or not.    

        Additional keyword arguments can be provided and will be forwarded directly to 
        the tool that becomes associated with the sources. Keys and values are tool specific. 
        """
        class _LazySource(object):
            def __init__(self, path, regex, recurse, filter, tool, **kwargs):
                self.path = path
                self.regex = regex
                self.recurse = recurse
                self.filter = filter
                self.tool = tool
                self.kwargs = kwargs
                self._sources = None

            @property
            def sources(self):
                if self._sources is not None:
                    return self._sources
                all_files = [path]
                if os.path.isdir(path):
                    if recurse:
                        all_files = [os.path.join(base, file) for base, dirs, files in os.walk(path) for file in files]
                    else:
                        all_files = os.listdir(path)
                        all_files = [os.path.join(path, file) for file in all_files]
                matching_files = [file for file in all_files if re.match(regex, file)]
                self._sources = [Source(source_file, filter, tool, kwargs) for source_file in matching_files]
                return self._sources
        if not files:
            self._sources.append(_LazySource(path, regex, recurse, filter, tool, **kwargs))
        else:
            for src in files:
                self._sources.append(Source(os.path.join(path, src), filter, tool, **kwargs))

    @property
    def sources(self):
        return [source for lazy_source in self._sources for source in lazy_source.sources]


class _Macro(_FilteredAndPublished):
    def __init__(self, key, value=None, filter=None, publish=False):
        super(_Macro, self).__init__(filter, publish)
        self.key = key
        self.value = value


class MacroGroup(object):
    """ A collection of preprocessor macros. """
    def __init__(self):
        super(MacroGroup, self).__init__()
        self.macros = []
    
    def add_macro(self, macro, value=None, filter=None, publish=False):
        """ Add a preprocessor **macro** to the group with an optional
        **value**. 
        
        The **filter** regex makes it possible to add macros conditionally for a
        specific toolchain. The regex is matched against the toolchain
        identifier to determine if macros should be applied or not.

        If **publish** is True, the macro will be inherited to projects
        depending on the project to which this group belongs.  
        """
        self.macros.append(_Macro(macro, value, filter, publish))


def has_macros(project):
    return isinstance(project, MacroGroup)


class _IncludePath(_FilteredAndPublished):
    def __init__(self, path, filter=None, publish=None):
        super(_IncludePath, self).__init__(filter, publish)
        self.path = path


class IncludePathGroup(object):
    def __init__(self):
        super(IncludePathGroup, self).__init__()
        self.incpaths = []

    def add_incpath(self, path, filter=None, publish=None):
        self.incpaths.append(_IncludePath(path, filter, publish)) 


class _LibraryPath(_FilteredAndPublished):
    def __init__(self, path, filter=None, publish=None):
        super(_LibraryPath, self).__init__(filter, publish)
        self.path = path


class LibraryPathGroup(object):
    def __init__(self):
        super(LibraryPathGroup, self).__init__()
        self.libpaths = []

    def add_libpath(self, path, filter=None, publish=None):
        self.libpaths.append(_LibraryPath(path, filter, publish))


class _Library(_FilteredAndPublished):
    def __init__(self, name, filter=None, publish=None):
        super(_Library, self).__init__(filter, publish)
        self.name = name


class LibraryGroup(object):
    def __init__(self):
        super(LibraryGroup, self).__init__()
        self.libraries = []

    def add_library(self, name, filter=None, publish=None):
        self.libraries.append(_Library(name, filter, publish))


class _Dependency(_FilteredAndPublished):
    def __init__(self, project, filter=None, publish=False):
        super(_Dependency, self).__init__(filter, publish)
        self.project = project


class DependencyGroup(object):
    def __init__(self):
        super(DependencyGroup, self).__init__()
        self.dependencies = []

    def add_dependency(self, project, filter=None, publish=None):
        self.dependencies.append(_Dependency(project, filter, publish))
        for dep in project.dependencies:
            self.dependencies.append(dep)


class _Feature(_Filtered):
    def __init__(self, name, filter=None, **kwargs):
        super(_Feature, self).__init__(filter)
        self.name = name
        self.args = kwargs
        
    def add_argument(self, **kwargs):
        self.args.update(kwargs)


class FeatureGroup(object):
    def __init__(self):
        super(FeatureGroup, self).__init__()
        self.features = []

    def use_feature(self, feature_name, filter=None, **kwargs):
        feature = _Feature(feature_name, filter, **kwargs)
        self.features.append(feature)
        return feature


class _Command(_Filtered):
    def __init__(self, output, inputs, command, filter=None, **kwargs):
        super(_Command, self).__init__(filter)
        self.output = output
        self.inputs = inputs if type(inputs) == list else [inputs]
        self.command = command
        self.args = kwargs
        
    def add_argument(self, **kwargs):
        self.args.update(kwargs)

    @property
    def cmdline(self):
        return self.command.format(inputs=" ".join(self.inputs), output=self.output)


class CommandGroup(object):
    def __init__(self):
        super(CommandGroup, self).__init__()
        self.commands = []

    def add_command(self, output, inputs, command, filter=None, **kwargs):
        self.commands.append(
            _Command(output, inputs, command, filter))


class ProjectRegistry(object):
    _projects = {}

    @staticmethod
    def add(project):
        # print("Registering project: {}".format(project.name))
        ProjectRegistry._projects[project.name] = project

    @staticmethod
    def find(project):
        if project not in ProjectRegistry._projects:
            raise ValueError(project) 
        return ProjectRegistry._projects[project]

    @staticmethod
    def all():
        return ProjectRegistry._projects.values()


class ProjectLoader(Loader):
    def __init__(self, path):
        super(ProjectLoader, self).__init__("build.projects", path)


class Project(SourceGroup, FeatureGroup):
    def __init__(self, name):
        super(Project, self).__init__(name)
        self._toolchain_groups = [ToolchainGroup()]
        self._source_groups = []
        self.uuid = str(uuid.uuid4())
        ProjectRegistry.add(self)

    def add_toolchain_group(self, toolchain_group):
        self._toolchain_groups.append(toolchain_group)

    def add_toolchain(self, toolchain):
        self._toolchain_groups[0].add_toolchain(toolchain)

    @property
    def toolchains(self):
        return [toolchain for group in self._toolchain_groups for toolchain in group.toolchains]

    @property
    def is_toolchain_agnostic(self):
        return False
    
    def new_source_group(self, name):
        group = SourceGroup(name)
        self.source_groups.append(group)
        return group

    def add_source_group(self, group):
        self.source_groups.append(group)
        return group

    @property
    def source_groups(self):
        return self._source_groups

    def add_feature_group(self, feature_group):
        for feature in feature_group.features:
            self.features.append(feature)

    def transform(self, toolchain):
        toolchain.transform(self)


class CSProject(Project, DependencyGroup):
    def __init__(self, name):
        super(CSProject, self).__init__(name)

    def add_dependency_group(self, dependency_group):
        for dependency in dependency_group.dependencies:
            self.dependencies.append(feature)


class CSLibrary(CSProject):
    def __init__(self, name):
        super(CSLibrary, self).__init__(name)


class CSExecutable(CSProject):
    def __init__(self, name):
        super(CSExecutable, self).__init__(name)


class CXXProject(Project, MacroGroup, IncludePathGroup, LibraryGroup, LibraryPathGroup, DependencyGroup, CommandGroup):
    def __init__(self, name):
        super(CXXProject, self).__init__(name)

    def add_dependency_group(self, dependency_group):
        for dependency in dependency_group.dependencies:
            self.dependencies.append(dependency)

    def add_macro_group(self, macro_group):
        for macro in macro_group.macros:
            self.macros.append(macro)

    def add_incpath_group(self, include_path_group):
        for include_path in include_path_group.incpaths:
            self.incpaths.append(include_path)

    def add_libpath_group(self, library_path_group):
        for library_path in library_path_group.libpaths:
            self.libpaths.append(library_path)

    def add_library_group(self, library_group):
        for library in library_group.libraries:
            self.libraries.append(library)

    def get_macros(self, toolchain=None, inherited=False):
        macros = [] + self.macros
        if inherited:
            for dep in self.dependencies:
                if hasattr(dep.project, "get_macros"):
                    macros += [macro for macro in dep.project.get_macros(toolchain, inherited) if macro.publish]
        return macros if toolchain is None else \
            [macro for macro in macros if macro.matches(toolchain.name)]

    def get_incpaths(self, toolchain=None, inherited=False):
        incpaths = [] + self.incpaths
        if inherited:
            for dep in self.dependencies:
                if hasattr(dep.project, "get_incpaths"):
                    incpaths += [path for path in dep.project.get_incpaths(toolchain, inherited) if path.publish]
        return incpaths if toolchain is None else \
            [incpath for incpath in incpaths if incpath.matches(toolchain.name)]

    def get_libraries(self, toolchain=None, inherited=False):
        libraries = [] + self.libraries
        if inherited:
            for dep in self.dependencies:
                if hasattr(dep.project, "get_libraries"):
                    libraries += [lib for lib in dep.project.get_libraries(toolchain, inherited) if lib.publish]
        return libraries if toolchain is None else \
            [lib for lib in libraries if lib.matches(toolchain.name)]
    
    def get_libpaths(self, toolchain=None, inherited=False):
        libpaths = [] + self.libpaths
        if inherited:
            for dep in self.dependencies:
                if hasattr(dep.project, "get_libpaths"):
                    libpaths += [path for path in dep.project.get_libpaths(toolchain, inherited) if path.publish]
        return libpaths if toolchain is None else \
            [libpath for libpath in libpaths if libpath.matches(toolchain.name)]

    def get_dependencies(self, toolchain=None):
        deps = [] + self.dependencies
        return deps if toolchain is None else \
            [dep for dep in deps if dep.matches(toolchain.name)]

    def get_commands(self, toolchain=None):
        cmds = [] + self.commands
        return cmds if toolchain is None else \
            [cmd for cmd in cmds if cmd.matches(toolchain.name)]

            

class CXXLibrary(CXXProject):
    def __init__(self, name, shared=False, external=False):
        """ Initialized a new C++ native library project called **name** """
        super(CXXLibrary, self).__init__(name)
        self.shared = shared
        self.external = external


class CXXExecutable(CXXProject):
    def __init__(self, name):
        """ Initialized a new C++ native executable project called **name** """
        super(CXXExecutable, self).__init__(name)



import urllib
import sys
import shutil
import zipfile
import tarfile


class PythonProject(Project):
    def __init__(self, name):
        super(PythonProject, self).__init__(name)

    @property
    def is_toolchain_agnostic(self):
        return True


class URLPackage(PythonProject, DependencyGroup):
    def __init__(self, name, url):
        super(URLPackage, self).__init__(name)
        self.url = url

    def _report(self, *args, **kwargs):
        sys.stdout.write(".")
        sys.stdout.flush()

    def _extract_zip(self, filename):
        with zipfile.ZipFile(filename) as zf:
            zf.extractall(self._location())

    def _extract_tar(self, filename):
        with tarfile.open(filename) as zf:
            zf.extractall(self._location())

    def _location(self):
        return "output/{}".format(self.name)
            
    def transform(self, toolchain):
        if os.path.exists(self._location()):
            return
        
        sys.stdout.write("Downloading...")
        sys.stdout.flush()
        urlopener = urllib.FancyURLopener()
        filename, headers = urlopener.retrieve(self.url, reporthook=self._report)
        print(filename)

        extractors = {
            ".zip": self._extract_zip,
            ".tar.gz": self._extract_tar,
            ".tgz": self._extract_tar,
            ".gz": self._extract_tar
        }

        _, ext = os.path.splitext(filename)
        if ext not in extractors:
            raise RuntimeError("unrecognized file format: {}".format(ext))

        sys.stdout.write("Extracting...")
        sys.stdout.flush()
        extractors[ext](filename)


class GitClone(PythonProject, DependencyGroup):
    def __init__(self, name, url, path=None):
        super(GitClone, self).__init__(name)
        self.url = url
        self.path = "{}/{}".format(name, path) if path else name

    def _location(self):
        return "output/{}".format(self.path)
            
    def transform(self, toolchain):
        if os.path.exists(self._location()):
            return

        sys.stdout.write("Cloning...")
        sys.stdout.flush()
        rc, stdout, stderr = utils.execute("git clone {} {}".format(self.url, self._location()))
        if rc != 0:
            print(stdout)
            print(stderr)
            raise RuntimeError("git clone failed")
