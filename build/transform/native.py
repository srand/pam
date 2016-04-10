from build import  model
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
        #print '\t', self.cmdline
        rc, stdout = utils.execute(self._cmdline, self._env)
        if rc != 0: raise RuntimeError('job failed')
        self._completed = True


class Object(Command):
    def __init__(self, product, cmdline, info=None, env=None):
        super(Object, self).__init__(product, cmdline, info, env)


class MSVCDirectory(Command):
    def __init__(self, product):
        cmdline = "cmd /c if not exist \"{dir}\" mkdir \"{dir}\"".format(dir=product)
        super(MSVCDirectory, self).__init__(product, cmdline)


class MSVCDriver(object):
    def _directory(self, cxx_project, object_file):
        dirname = path.dirname(object_file)
        job = cxx_project.get_job(dirname)
        if not job:
            job = MSVCDirectory(dirname)
            cxx_project.add_job(job)
        return job     


class MSVCCompilerDriver(MSVCDriver):
    def __init__(self, cxx=False, env=None):
        self._executable = "cl.exe"
        self._output_ext = ".obj"
        self._cxx = cxx
        self._env = env
        
    def _product(self, cxx_project, source_file):
        return '{output}{}{}'.format(source_file, self._output_ext, output=cxx_project.output)
        
    def _cmdline(self, cxx_project, source_file):
        def key_value(key, value):
            return "{}".format(key) if value is None else "{}={}".format(key, value)
		
        definitions = ['/D{}'.format(key_value(key, value)) for key, value in cxx_project.macros ]
        incpaths = ['/I{}'.format(path) for path in cxx_project.incpaths]
        flags = cxx_project.cflags if not self._cxx else cxx_project.cxxflags

        return "{} /nologo {} {} {} /c /T{}{} /Fo{}".format(
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
        dir = self._directory(cxx_project, product)
        obj =  Object(product, 
                      self._cmdline(cxx_project, source_file.path), 
                      self._info(source_file.path),
                      self._env)
        cxx_project.add_job(Source(source_file.path))
        cxx_project.add_job(obj)
        cxx_project.add_dependency(obj.product, source_file.path)
        cxx_project.add_dependency(obj.product, dir.product)


class MSVCLinkerDriver(MSVCDriver):
    def __init__(self, env=None):
        self._executable = 'link.exe'
        self._output_ext = '.exe'
        self._env = env

    def _product(self, cxx_project):
        return '{output}{}{}'.format(cxx_project.name, self._output_ext, output=cxx_project.output)

    def _cmdline(self, cxx_project, object_files):
        libpaths = ['/libpath:{}'.format(path) for path in cxx_project.libpaths]
        libraries = ['{output}/{lib}/{lib}.lib'.format(output=cxx_project.toolchain.output, lib=lib) for lib in cxx_project.libraries]
        flags = cxx_project.linkflags

        return "{} /nologo {} {} {} {} /out:{}".format(
            self._executable, 
            ' '.join(libpaths),
            ' '.join(libraries),
            ' '.join(flags),
            ' '.join(object_files),
            self._product(cxx_project))

    def _info(self, cxx_project):
        return ' [{}] {}'.format(self._executable.upper(), cxx_project.name)

    def transform(self, cxx_project, object_files):
        product = self._product(cxx_project)
        dir = self._directory(cxx_project, product)
        executable = Object(product, 
                            self._cmdline(cxx_project, object_files), 
                            self._info(cxx_project),
                            self._env)
        cxx_project.add_job(executable)                            
        cxx_project.add_dependency(executable.product, dir.product)
        for obj in object_files:
            cxx_project.add_dependency(executable.product, obj)


class MSVCArchiverDriver(MSVCDriver):
    def __init__(self, env=None):
        self._executable = 'lib.exe'
        self._output_pfx = ''
        self._output_ext = '.lib'
        self._env = env

    def _product(self, cxx_project):
        return '{output}{}{}{}'.format(self._output_pfx, cxx_project.name, self._output_ext, output=cxx_project.output)

    def _cmdline(self, cxx_project, object_files):
        return "{} /nologo /out:{} {}".format(
            self._executable,
            self._product(cxx_project), 
            ' '.join(object_files))

    def _info(self, cxx_project):
        return ' [{}] {}'.format(self._executable.upper(), cxx_project.name)

    def transform(self, cxx_project, object_files):
        product = self._product(cxx_project)
        dir = self._directory(cxx_project, product)
        library = Object(product, 
                         self._cmdline(cxx_project, object_files), 
                         self._info(cxx_project),
                         self._env)
        cxx_project.add_job(library)
        cxx_project.add_dependency(library.product, dir.product)
        for obj in object_files:
            cxx_project.add_dependency(library.product, obj)


class GNUCompilerDriver(object):
    def __init__(self, cxx=False, executable='gcc'):
        self._executable = executable
        self._cxx = cxx
        self._output_ext = '.o'

    def _product(self, source_file):
        return '{}{}'.format(source_file, self._output_ext)

    def _cmdline(self, settings, source_file):
        def key_value(key, value):
            return "{}".format(key) if value is None else "{}={}".format(key, value)
		
        definitions = ['-D{}'.format(key_value(key, value)) for key, value in settings.macros ]
        incpaths = ['-I{}'.format(path) for path in settings.incpaths]
        flags = settings.cflags if not self._cxx else settings.cxxflags

        return "{} {} {} {} -c {} -o {}".format(
            self._executable, 
            ' '.join(flags),
            ' '.join(definitions),
            ' '.join(incpaths),
            source_file, 
            self._product(source_file))

    def _info(self, source_file):
        return ' [{}] {}'.format(self._executable.upper(), source_file)

    def transform(self, cxx_project, source_file):
        obj =  Object(self._product(source_file.path), 
                      self._cmdline(cxx_project, source_file.path), 
                      self._info(source_file.path))
        cxx_project.add_job(Source(source_file.path))
        cxx_project.add_job(obj)
        cxx_project.add_dependency(obj.product, source_file.path)


class GNULinkerDriver(object):
    def __init__(self, cxx=False, executable='gcc'):
        self._executable = executable
        self._cxx = cxx
        self._output_ext = ''

    def _product(self, executable):
        return '{}{}'.format(executable, self._output_ext)

    def _cmdline(self, settings, executable, object_files):
        libpaths = ['-L{}'.format(path) for path in settings.libpaths]
        libraries = ['-l{}'.format(path) for path in settings.libraries]
        flags = settings.linkflags

        return "{} {} {} {} {} -o {}".format(
            self._executable, 
            ' '.join(libpaths),
            ' '.join(libraries),
            ' '.join(flags),
            ' '.join(object_files),
            self._product(executable))

    def _info(self, executable):
        return ' [{}] {}'.format(self._executable.upper(), executable)

    def transform(self, cxx_project, object_files):
        executable = Object(self._product(cxx_project.name), 
                            self._cmdline(cxx_project, executable, object_files), 
                            self._info(cxx_project.name))
        cxx_project.add_job(executable)
        for obj in object_files:
            cxx_project.add_dependency(executable.product, obj)


class GNUArchiverDriver(object):
    def __init__(self):
        self._executable = 'ar'
        self._output_pfx = 'lib'
        self._output_ext = '.a'

    def _product(self, name):
        return '{}{}{}'.format(self._output_pfx, name, self._output_ext)

    def _cmdline(self, name, object_files):
        return "{} cr {} {}".format(self._executable, self._product(name), ' '.join(object_files))

    def _info(self, name):
        return ' [{}] {}'.format(self._executable.upper(), name)

    def transform(self, cxx_project, object_files):
        library = Object(self._product(cxx_project.name), 
                         self._cmdline(cxx_project.name, object_files), 
                         self._info(cxx_project.name))
        cxx_project.add_job(library)
        for obj in object_files:
            cxx_project.add_dependency(library.product, obj)


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

    def transform(self, project):
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
            self.archiver.transform(cxx_project, object_names)

        if isinstance(project, model.CXXExecutable):
            objects = cxx_project.objects
            object_names = [obj.product for obj in objects]
            self.linker.transform(cxx_project, object_names)
                        
        cxx_project.transform()
        

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


class MSVCCXXToolchain(CXXToolchain):
    def __init__(self, name, env=None):
        super(MSVCCXXToolchain, self).__init__(name)
        self.add_tool('.s', MSVCCompilerDriver(env=env))
        self.add_tool('.c', MSVCCompilerDriver(env=env))
        self.add_tool('.cc', MSVCCompilerDriver(cxx=True, env=env))
        self.add_tool('.cpp', MSVCCompilerDriver(cxx=True, env=env))
        self.archiver = MSVCArchiverDriver(env=env)
        self.linker = MSVCLinkerDriver(env=env)


class GNUCXXToolchain(CXXToolchain):
    def __init__(self, name):
        super(GNUCXXToolchain, self).__init__(name)
        self.add_tool('.S', GNUCompilerDriver(cxx=False, executable='gcc'))
        self.add_tool('.c', GNUCompilerDriver(cxx=False, executable='gcc'))
        self.add_tool('.cc', GNUCompilerDriver(cxx=True, executable='g++'))
        self.add_tool('.cpp', GNUCompilerDriver(cxx=True, executable='g++'))
        self.archiver = GNUArchiverDriver()
        self.linker = GNULinkerDriver(cxx=True, executable='g++')


class ClangCXXToolchain(CXXToolchain):
    def __init__(self, name):
        super(ClangCXXToolchain, self).__init__(name)
        self.add_tool('.S', GNUCompilerDriver(cxx=False, executable='clang'))
        self.add_tool('.c', GNUCompilerDriver(cxx=False, executable='clang'))
        self.add_tool('.cc', GNUCompilerDriver(cxx=True, executable='clang++'))
        self.add_tool('.cpp', GNUCompilerDriver(cxx=True, executable='clang++'))
        self.archiver = GNUArchiverDriver()
        self.linker = GNULinkerDriver(cxx=True, executable='clang++')
