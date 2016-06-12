from build import model
from build.transform import utils
from build.transform.toolchain import Toolchain
from copy import copy
from os import path


class Settings(object):
    def __init__(self, template_settings=None):
        if template_settings:
            self._macros = copy(template_settings._macros)
            self._incpaths = copy(template_settings._incpaths)
            self._libpaths = copy(template_settings._libpaths)
            self._cflags = copy(template_settings._cflags)
            self._cxxflags = copy(template_settings._cxxflags)
            self._linkflags = copy(template_settings._linkflags)
            self._libraries = copy(template_settings._libraries)
        else:
            self._macros = set()
            self._incpaths = set()
            self._libpaths = set()
            self._cflags = []
            self._cxxflags = []
            self._linkflags = []
            self._libraries = []

    def add_macro(self, name, value=None):
        self._macros.add((name, value))

    @property
    def macros(self):
        return self._macros

    def add_incpath(self, path):
        self._incpaths.add(path)

    @property
    def incpaths(self):
        return self._incpaths

    def add_libpath(self, path):
        if not path:
            self._libpaths.add('.')
        else:
            self._libpaths.add(path)

    @property
    def libpaths(self):
        return self._libpaths

    def add_cflag(self, *flags):
        for flag in flags:
            self._cflags.append(flag)

    @property
    def cflags(self):
        return self._cflags

    def add_cxxflag(self, *flags):
        for flag in flags:
            self._cxxflags.append(flag)

    @property
    def cxxflags(self):
        return self._cxxflags

    def add_linkflag(self, *flags):
        for flag in flags:
            self._linkflags.append(flag)

    @property
    def linkflags(self):
        return self._linkflags

    def add_library(self, lib):
        self._libraries.append(lib)

    @property
    def libraries(self):
        return self._libraries


class Job(object):
    def __init__(self, product, driver=None):
        self._product = product
        self._driver = driver
        self._completed = False
        self._deps = {}

    @property
    def product(self):
        return self._product

    @property
    def driver(self):
        return self._driver

    @property
    def completed(self):
        return self._completed

    @property
    def required(self):
        required_deps = [dep for dep in self._deps.values() if dep.required]
        return not self.completed or required_deps

    def add_dependency(self, job):
        self._deps[job.product] = job
        
    def dependencies(self):
        return self._deps.keys()

    def execute(self):
        if self.driver:
            driver.execute(product, self)


class Source(Job):
    def __init__(self, source):
        super(Source, self).__init__(source)


class Command(Job):
    def __init__(self, product, cmdline, info=None, env=None):
        super(Command, self).__init__(product)
        self._cmdline = cmdline
        self._info = info
        self._env = env

    @property
    def cmdline(self):
        return self._cmdline

    @property 
    def info(self):
        return self._info

    def execute(self):
        if self.completed: return

        required_deps = [dep for dep in self._deps.values() if dep.required]
        for dep in required_deps:
            dep.execute()

        #print self.info
        print '\t', self.cmdline
        rc, stdout = utils.execute(self._cmdline, self._env)
        if rc != 0: raise RuntimeError('job failed')
        self._completed = True


class Object(Command):
    def __init__(self, product, cmdline, info=None, env=None):
        super(Object, self).__init__(product, cmdline, info, env)


class CXXToolchain(Toolchain, Settings):
    def __init__(self, name):
        super(CXXToolchain, self).__init__(name)
        self._tools = {}
        self._cxx_archiver = None
        self._cxx_linker = None
        self.output = "output/{}".format(name)

    def add_tool(self, extension, driver):
        self._tools[extension] = driver

    def get_tool(self, extension):
        if extension not in self._tools:
            raise RuntimeError('could not find tool for {} extension'.format(extension))
        return self._tools[extension]
        
    @property
    def archiver(self):
        return self._cxx_archiver

    @archiver.setter
    def archiver(self, archiver):
        self._cxx_archiver = archiver
        
    @property
    def linker(self):
        return self._cxx_linker

    @linker.setter
    def linker(self, linker_driver):
        self._cxx_linker = linker_driver

    def generate(self, project):
        cxx_project = CXXProject(self, project.name)
        
        macros = [macro for macro in project.macros if macro.matches(self.name)]
        incpaths = [incpath for incpath in project.incpaths if incpath.matches(self.name)]
        libpaths = [libpath for libpath in project.libpaths if libpath.matches(self.name)]

        if isinstance(project, model.CXXExecutable):
            macros += [macro for dep in project.dependencies for macro in dep.macros if macro.publish]
            incpaths += [incpath for dep in project.dependencies for incpath in dep.incpaths if incpath.publish]
            libpaths += [libpath for dep in project.dependencies for libpath in dep.libpaths if libpath.publish]

        for macro in macros:
            cxx_project.add_macro(macro.key, macro.value)    
        for incpath in incpaths:
            cxx_project.add_incpath(incpath.path)    
        for libpath in libpaths:
            cxx_project.add_libpath(libpath.path)    

        for dep in project.dependencies:
            if isinstance(dep, model.CXXLibrary):
                cxx_project.add_library(dep.name)            

        self.apply_features(project, cxx_project)            

        groups = project.source_groups + [project]
        for group in groups:
            for source in group.sources:
                tool = self.get_tool(source.tool)
                if tool is None:
                    raise RuntimeError()
                tool.transform(cxx_project, source)

        if isinstance(project, model.CXXLibrary):
            objects = cxx_project.objects
            object_names = [obj.product for obj in objects]
            cxx_project.job = self.archiver.transform(cxx_project, object_names)

        if isinstance(project, model.CXXExecutable):
            objects = cxx_project.objects
            object_names = [obj.product for obj in objects]
            cxx_project.job = self.linker.transform(cxx_project, object_names)
            
        return cxx_project
            
    def transform(self, project):
        self.generate(project).transform()


class CXXProject(Settings):
    def __init__(self, toolchain, name):
        super(CXXProject, self).__init__(toolchain)
        self._jobs = {}
        self.name = name
        self.toolchain = toolchain
        self.output = "{output}/{name}/".format(output=toolchain.output, name=name)
        
    @property
    def objects(self):
        return [job for job in self._jobs.values() if isinstance(job, Object)]

    @property
    def commands(self):
        return [job for job in self._jobs.values() if isinstance(job, Command)]

    def add_command(self, product, cmdline=None, info=None):
        if product in self._jobs:
            raise RuntimeError('already know about {}'.format(product))
        job = self._jobs[product] = Command(product, cmdline, info)
        return job

    def add_job(self, job):
        if job.product in self._jobs:
            raise RuntimeError('already know about {}'.format(product))
        self._jobs[job.product] = job
        return job

    def get_job(self, job):
        return self._jobs.get(job) 
       
    def add_dependency(self, product1, product2):
        if product1 not in self._jobs:
            raise RuntimeError('{} not known'.format(product1))
        if product2 not in self._jobs:
            raise RuntimeError('{} not known'.format(product2))
        job1, job2 = self._jobs[product1], self._jobs[product2]
        job1.add_dependency(job2)

    def transform(self):
        for product in self._jobs:
            job = self._jobs[product]
            if job.required:
                job.execute()
