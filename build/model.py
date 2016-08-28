from build.utils import Loader
import os
import re
import uuid


class _Filtered(object):
    def __init__(self, filter):
        super(_Filtered, self).__init__()
        self.filter = filter
        
    def matches(self, string):
        if self.filter is None:
            return True
        return re.search(self.filter, string) is not None


class _FilteredAndPublished(_Filtered):
    def __init__(self, filter, publish):
        super(_FilteredAndPublished, self).__init__(filter)
        self.publish = publish


class Toolchain(object):
    def __init__(self, name):
        self.name = name


class ToolchainGroup(object):
    def __init__(self):
        super(ToolchainGroup, self).__init__()
        self.toolchains = []

    def add_toolchain(self, toolchain):
        self.toolchains.append(toolchain)


class Source(_Filtered):
    def __init__(self, path, filter=None, tool=None, args=None):
        super(Source, self).__init__(filter)
        self.path = os.path.normpath(path)
        self.args = args
        _, self.tool = (None, tool) if tool is not None else os.path.splitext(self.path)


class SourceGroup(object):
    def __init__(self, name=None):
        super(SourceGroup, self).__init__()
        self.sources = []
        self.name = name

    def add_sources(self, path, regex=r'.*', recurse=False, filter=None, tool=None, **kwargs):
        all_files = [path]
        if os.path.isdir(path):
            if recurse:
                all_files = [os.path.join(base, file) for base, dirs, files in os.walk(path) for file in files]
            else:
                all_files = os.listdir(path)
                all_files = [os.path.join(path, file) for file in all_files]

        matching_files = [file for file in all_files if re.match(regex, file)]
        for source_file in matching_files:
            self.sources.append(Source(source_file, filter, tool, kwargs))


class Macro(_FilteredAndPublished):
    def __init__(self, key, value=None, filter=None, publish=None):
        super(Macro, self).__init__(filter, publish)
        self.key = key
        self.value = value


class MacroGroup(object):
    def __init__(self):
        super(MacroGroup, self).__init__()
        self.macros = []
    
    def add_macro(self, key, value=None, filter=None, publish=None):
        self.macros.append(Macro(key, value, filter, publish)) 


class IncludePath(_FilteredAndPublished):
    def __init__(self, path, filter=None, publish=None):
        super(IncludePath, self).__init__(filter, publish)
        self.path = path


class IncludePathGroup(object):
    def __init__(self):
        super(IncludePathGroup, self).__init__()
        self.incpaths = []

    def add_incpath(self, path, filter=None, publish=None):
        self.incpaths.append(IncludePath(path, filter, publish)) 


class LibraryPath(_FilteredAndPublished):
    def __init__(self, path, filter=None, publish=None):
        super(LibraryPath, self).__init__(filter, publish)
        self.path = path


class LibraryPathGroup(object):
    def __init__(self):
        super(LibraryPathGroup, self).__init__()
        self.libpaths = []

    def add_libpath(self, path, filter=None, publish=None):
        self.libpaths.append(LibraryPath(path, filter, publish)) 


class DependencyGroup(object):
    def __init__(self):
        super(DependencyGroup, self).__init__()
        self.dependencies = []

    def add_dependency(self, project, filter=None, publish=None):
        for dep in project.dependencies:
            self.dependencies.append(dep)
        self.dependencies.append(project) 


class Feature(_Filtered):
    def __init__(self, name, filter=None):
        super(Feature, self).__init__(filter)
        self.name = name


class FeatureGroup(object):
    def __init__(self):
        super(FeatureGroup, self).__init__()
        self.features = []

    def add_feature(self, feature_name, filter=None):
        self.features.append(Feature(feature_name, filter))


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


class CXXProject(Project, MacroGroup, IncludePathGroup, LibraryPathGroup, DependencyGroup):
    def __init__(self, name):
        super(CXXProject, self).__init__(name)

    def add_dependency_group(self, dependency_group):
        for dependency in dependency_group.dependencies:
            self.dependencies.append(dependency)

    def add_macro_group(self, macro_group):
        for macro in macro_group.macros:
            self.macros.append(macro)

    def add_include_path_group(self, include_path_group):
        for include_path in include_path_group.incpaths:
            self.incpaths.append(include_path)

    def add_library_path_group(self, library_path_group):
        for library_path in library_path_group.libpaths:
            self.libpaths.append(library_path)


class CXXLibrary(CXXProject):
    def __init__(self, name):
        super(CXXLibrary, self).__init__(name)


class CXXExecutable(CXXProject):
    def __init__(self, name):
        super(CXXExecutable, self).__init__(name)
