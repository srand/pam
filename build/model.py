from build.feature import FeatureRegistry
from build.utils import Loader
import os
import re
import uuid


class _Filtered(object):
    def __init__(self, filter):
        self.filter = filter
        
    def matches(self, string):
        if self.filter is None:
            return True
        return re.search(self.filter, string) is not None


class _FilteredAndPublished(_Filtered):
    def __init__(self, filter, publish):
        super(_FilteredAndPublished, self).__init__(filter)
        self.publish = publish


class Source(_Filtered):
    def __init__(self, path, filter=None, tool=None, args=None):
        super(Source, self).__init__(filter)
        self.path = path
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


class IncludePath(_FilteredAndPublished):
    def __init__(self, path, filter=None, publish=None):
        super(IncludePath, self).__init__(filter, publish)
        self.path = path


class LibraryPath(_FilteredAndPublished):
    def __init__(self, path, filter=None, publish=None):
        super(LibraryPath, self).__init__(filter, publish)
        self.path = path


class Feature(_Filtered):
    def __init__(self, name, filter=None):
        super(Feature, self).__init__(filter)
        self.name = name


class ProjectRegistry(object):
    _projects = {}
    
    @staticmethod
    def add(project):
        print("Registering project: {}".format(project.name))
        ProjectRegistry._projects[project.name] = project
        
    @staticmethod
    def find(project):
        if project not in ProjectRegistry._projects:
            raise ValueError(project) 
        return ProjectRegistry._projects[project]


class ProjectLoader(Loader):
    def __init__(self, path):
        super(ProjectLoader, self).__init__("build.projects", path)


class Project(SourceGroup):
    def __init__(self, name):
        super(Project, self).__init__(name)
        self._source_groups = []
        self._features = []        
        self.uuid = str(uuid.uuid4())
        ProjectRegistry.add(self)

    def add_source_group(self, group):
        self.source_groups.append(group)
        
    @property
    def source_groups(self):
        return self._source_groups
        
    def add_feature(self, feature_name, filter=None):
        self._features.append(Feature(feature_name, filter))

    @property
    def features(self):
        return self._features
        
    def transform(self, toolchain):
        toolchain.transform(self)


class CXXProject(Project):
    def __init__(self, name):
        super(CXXProject, self).__init__(name)
        self.incpaths = []
        self.libpaths = []
        self.macros = []
        self.dependencies = []

    def add_dependency(self, project, filter=None, publish=None):
        for dep in project.dependencies:
            self.dependencies.append(dep)
        self.dependencies.append(project) 
       
    def add_incpath(self, path, filter=None, publish=None):
        self.incpaths.append(IncludePath(path, filter, publish)) 

    def add_libpath(self, path, filter=None, publish=None):
        self.libpaths.append(LibraryPath(path, filter, publish)) 

    def add_macro(self, key, value=None, filter=None, publish=None):
        self.macros.append(Macro(key, value, filter, publish)) 


class CXXLibrary(CXXProject):
    def __init__(self, name):
        super(CXXLibrary, self).__init__(name)


class CXXExecutable(CXXProject):
    def __init__(self, name):
        super(CXXExecutable, self).__init__(name)
