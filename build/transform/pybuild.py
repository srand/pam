##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


import build
from build import model
from build.transform import utils
from build.transform.toolchain import Toolchain
from copy import copy
from os import path, stat


class Settings(object):
    def __init__(self, template_settings=None):
        if template_settings:
            self._cflags = copy(template_settings._cflags)
            self._cxxflags = copy(template_settings._cxxflags)
            self._linkflags = copy(template_settings._linkflags)
            self._libraries = copy(template_settings._libraries)
        else:
            self._cflags = []
            self._cxxflags = []
            self._linkflags = []
            self._libraries = []

    def add_cflag(self, *flags):
        for flag in flags:
            if flag not in self._cflags:
                self._cflags.append(flag)

    @property
    def cflags(self):
        return self._cflags

    def add_cxxflag(self, *flags):
        for flag in flags:
            if flag not in self._cxxflags:
                self._cxxflags.append(flag)

    @property
    def cxxflags(self):
        return self._cxxflags

    def add_linkflag(self, *flags):
        for flag in flags:
            if flag not in self._linkflags:
                self._linkflags.append(flag)

    @property
    def linkflags(self):
        return self._linkflags

    def add_library(self, lib):
        if lib not in self._libraries:
            self._libraries.append(lib)

    @property
    def libraries(self):
        return self._libraries


class Job(object):
    def __init__(self, product, driver=None):
        self._product = path.normpath(product)
        self._driver = driver
        self._completed = False
        self._deps = {}
        self._timestamp = 0
        self._required = None

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
        if self._required is None:
            deps_timestamp = max([dep.timestamp for dep in self._deps.values()] + [0])
            deps_required = [dep for dep in self._deps.values() if dep.required]
            self._required = deps_required or deps_timestamp > self.timestamp
        return self._required 

    @property
    def timestamp(self):
        if path.exists(self.product):
            s = stat(self.product)
            if s: self._timestamp = s.st_mtime
        return self._timestamp

    def add_dependency(self, job):
        self._deps[job.product] = job

    def get_dependency(self, name):
        return self._deps[name]
        
    def dependencies(self):
        return self._deps.keys()

    def execute(self):
        if self.completed: 
            return
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
        if build.verbose:
            utils.print_locked(self._cmdline)
        rc, stdout, stderr = utils.execute(self._cmdline, self._env, output=False)
        if rc != 0: 
            utils.print_locked("{}", "\n".join(stdout))
            utils.print_locked("{}", "\n".join(stderr))
            raise RuntimeError('job failed: ' + self._cmdline)
        self._completed = True


class Object(Command):
    def __init__(self, product, cmdline, info=None, env=None):
        super(Object, self).__init__(product, cmdline, info, env)


class CXXToolchain(Toolchain):
    def __init__(self, name):
        super(CXXToolchain, self).__init__(name)
        self._tools = {}
        self._cxx_archiver = None
        self._cxx_linker = None

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

    def generate(self, project, toolchain=None):
        toolchain = toolchain if toolchain else self
        cxx_project = CXXProject(toolchain, project.name)
        cxx_project.toolchain.apply_features(project, cxx_project, toolchain)

        groups = project.source_groups + [project]
        for group in groups:
            for source in group.sources:
                if not source.matches(toolchain.name):
                    continue
                tool = toolchain.get_tool(source.tool)
                if tool is None:
                    raise RuntimeError()
                tool.transform(cxx_project, source)

        if isinstance(project, model.CXXLibrary):
            objects = cxx_project.objects
            object_names = [obj.product for obj in objects]
            if project.shared:
                archiver = toolchain.linker if hasattr(toolchain, 'linker') else self.linker
            else:
                archiver = toolchain.archiver if hasattr(toolchain, 'archiver') else self.archiver
            cxx_project.job = archiver.transform(project, cxx_project, object_names)

        if isinstance(project, model.CXXExecutable):
            objects = cxx_project.objects
            object_names = [obj.product for obj in objects]
            linker = toolchain.linker if hasattr(toolchain, 'linker') else self.linker
            cxx_project.job = linker.transform(project, cxx_project, object_names)
            
        return cxx_project
            
    def transform(self, project):
        return self.generate(project).transform()


class CXXProject(Settings):
    def __init__(self, toolchain, name):
        super(CXXProject, self).__init__()
        self._jobs = {}
        self.name = name
        self.toolchain = toolchain
        self.output = path.join(toolchain.attributes.output, name)
        
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
        return self._jobs.get(path.normpath(job)) 
       
    def add_dependency(self, product1, product2):
        if product1 not in self._jobs:
            raise RuntimeError('{} not known'.format(product1))
        if product2 not in self._jobs:
            raise RuntimeError('{} not known'.format(product2))
        job1, job2 = self._jobs[product1], self._jobs[product2]
        job1.add_dependency(job2)

    def transform(self):
        if not self.job.required: 
            return False
        jobs = {}
        consumes = {}
        for product, job in self._jobs.iteritems():
            jobs[product] = []
            consumes[product] = []

        # Build graph of inverse dependencies
        for product, job in self._jobs.iteritems():
            for depname in job.dependencies():
                dep = self._jobs[depname]
                jobs[product].append(dep)
                if dep.product not in consumes:
                    consumes[dep.product] = []    
                consumes[dep.product].append(job)
        
        # Process jobs
        pool = utils.Pool()
        while jobs:
            candidates = [self._jobs[product] for product, deplist in jobs.iteritems() if not deplist]
            for job in candidates:
                del jobs[job.product]
                pool.put(job) 

            completed = []
            try:
                job = pool.get()
                while job:
                    completed.append(job)
                    job = pool.get_nowait()
            except Exception as e:
                print(e)
                break

            for job in completed:
                for consumer in consumes[job.product]:
                    jobs[consumer.product].remove(job)

        pool.stop()
        return True
