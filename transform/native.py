from toolchain import Toolchain
import project as project_type
import os
import utils
from copy import copy


class Settings(object):
    def __init__(self, template_settings=None):
        if template_settings:
            self._defines = copy(template_settings._defines)
            self._incpaths = copy(template_settings._incpaths)
            self._libpaths = copy(template_settings._libpaths)
            self._cflags = copy(template_settings._cflags)
            self._cxxflags = copy(template_settings._cxxflags)
            self._linkflags = copy(template_settings._linkflags)
            self._libraries = copy(template_settings._libraries)
        else:
            self._defines = set()
            self._incpaths = set()
            self._libpaths = set()
            self._cflags = []
            self._cxxflags = []
            self._linkflags = []
            self._libraries = []

    def add_define(self, name, value=None):
        self._defines.add((name, value))

    @property
    def defines(self):
        return self._defines

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

        print self.info
        # print '\t', self.cmdline
        rc, stdout = utils.execute(self._cmdline, self._env)
        if rc != 0: raise RuntimeError('job failed')
        self._completed = True


class Object(Command):
    def __init__(self, product, cmdline, info=None, env=None):
        super(Object, self).__init__(product, cmdline, info, env)


class MSVCCompilerDriver(object):
    def __init__(self, cxx=False, env=None):
        self._executable = "cl.exe"
        self._output_ext = ".obj"
        self._cxx = cxx
        self._env = env
        
    def _product(self, source_file):
        return '{}{}'.format(source_file, self._output_ext)
        
    def _cmdline(self, settings, source_file):
        defines1 = ['/D{}'.format(name) for name, value in settings.defines if not value ]
        defines2 = ['/D{}={}'.format(name, value) for name, value in settings.defines if value ]
        flags = settings.cflags if not self._cxx else settings.cxxflags
        incpaths = ['/I{}'.format(path) for path in settings.incpaths]

        return "{} /nologo {} {} {} {} /c {} /Fo{}".format(
            self._executable, 
            ' '.join(flags),
            ' '.join(defines1),
            ' '.join(defines2),
            ' '.join(incpaths),
            source_file, 
            self._product(source_file))

    def _info(self, source_file):
        return ' [{}] {}'.format(self._executable.upper(), source_file)

    def prepare(self, settings, source_file):
        return Object(self._product(source_file), self._cmdline(settings, source_file), self._info(source_file), env=self._env)


class MSVCLinkerDriver(object):
    def __init__(self, env=None):
        self._executable = 'link.exe'
        self._output_ext = '.exe'
        self._env = env

    def _product(self, executable):
        return '{}{}'.format(executable, self._output_ext)

    def _cmdline(self, settings, executable, object_files):
        libpaths = ['/libpath:{}'.format(path) for path in settings.libpaths]
        libraries = ['{}.lib'.format(path) for path in settings.libraries]
        flags = settings.linkflags

        return "{} /nologo {} {} {} {} /out:{}".format(
            self._executable, 
            ' '.join(libpaths),
            ' '.join(libraries),
            ' '.join(flags),
            ' '.join(object_files),
            self._product(executable))

    def _info(self, executable):
        return ' [{}] {}'.format(self._executable.upper(), executable)

    def prepare(self, settings, executable, object_files):
        return Object(self._product(executable), self._cmdline(settings, executable, object_files), self._info(executable), env=self._env)


class MSVCArchiverDriver(object):
    def __init__(self, env=None):
        self._executable = 'lib.exe'
        self._output_pfx = ''
        self._output_ext = '.lib'
        self._env = env

    def _product(self, name):
        return '{}{}{}'.format(self._output_pfx, name, self._output_ext)

    def _cmdline(self, name, object_files):
        return "{} /nologo /out:{} {}".format(self._executable, self._product(name), ' '.join(object_files))

    def _info(self, name):
        return ' [{}] {}'.format(self._executable.upper(), name)

    def prepare(self, settings, name, object_files):
        return Object(self._product(name), self._cmdline(name, object_files), self._info(name), env=self._env)


class GNUCompilerDriver(object):
    def __init__(self, cxx=False, executable='gcc'):
        self._executable = executable
        self._cxx = cxx
        self._output_ext = '.o'

    def _product(self, source_file):
        return '{}{}'.format(source_file, self._output_ext)

    def _cmdline(self, settings, source_file):
        defines1 = ['-D{}'.format(name) for name, value in settings.defines if not value ]
        defines2 = ['-D{}={}'.format(name, value) for name, value in settings.defines if value ]
        flags = settings.cflags if not self._cxx else settings.cxxflags
        incpaths = ['-I{}'.format(path) for path in settings.incpaths]

        return "{} {} {} {} {} -c {} -o {}".format(
            self._executable, 
            ' '.join(flags),
            ' '.join(defines1),
            ' '.join(defines2),
            ' '.join(incpaths),
            source_file, 
            self._product(source_file))

    def _info(self, source_file):
        return ' [{}] {}'.format(self._executable.upper(), source_file)

    def prepare(self, settings, source_file):
        return Object(self._product(source_file), self._cmdline(settings, source_file), self._info(source_file))


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

    def prepare(self, settings, executable, object_files):
        return Object(self._product(executable), self._cmdline(settings, executable, object_files), self._info(executable))


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

    def prepare(self, settings, name, object_files):
        return Object(self._product(name), self._cmdline(name, object_files), self._info(name))


class CXXToolchain(Toolchain, Settings):
    def __init__(self):
        super(CXXToolchain, self).__init__()
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

    def transform(self, project):
        cxx_project = NativeCXXProject(self, project.name)
        
        for path in project.incpaths:
            cxx_project.add_incpath(path)
        for key, value in project.macros:
            cxx_project.add_define(key, value)
        for dep in project.dependencies:
            if isinstance(dep, project_type.Library):
                cxx_project.add_library(dep.name)            

        for source in project.sources:
            root, ext = os.path.splitext(source.path)
            tool = self.get_tool(ext)
            if tool is None:
                raise RuntimeError()
            cxx_project.add_job(tool.prepare(cxx_project, source.path))

        if isinstance(project, project_type.CXXLibrary):
            objects = cxx_project.objects
            object_names = [obj.product for obj in objects]
            library = self.archiver.prepare(cxx_project, cxx_project.name, object_names)
            cxx_project.add_job(library)
            for obj in objects:
                cxx_project.add_dependency(library.product, obj.product)

        if isinstance(project, project_type.CXXExecutable):
            objects = cxx_project.objects
            object_names = [obj.product for obj in objects]
            executable = self.linker.prepare(cxx_project, cxx_project.name, object_names)
            cxx_project.add_job(executable)
            for obj in objects:
                cxx_project.add_dependency(executable.product, obj.product)
                
        cxx_project.transform()
        

class NativeCXXProject(Settings):
    def __init__(self, settings, name):
        super(NativeCXXProject, self).__init__(settings)
        self._jobs = {}
        self.name = name
        
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


def VS2015Environment():
    env = copy(os.environ)

    installdir = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0'
    if not os.path.exists(installdir):
        raise RuntimeError('VS2015 is not installed')
        
    common7ide = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\Common7\IDE'
    vcbin = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN'
    common7tools = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\Common7\Tools'
    include = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE;C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\INCLUDE;C:\Program Files (x86)\Windows Kits\10\\include\10.0.10056.0\ucrt;C:\Program Files (x86)\Windows Kits\8.1\include\shared;C:\Program Files (x86)\Windows Kits\8.1\include\um;C:\Program Files (x86)\Windows Kits\8.1\include\winrt;'
    lib = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB;C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB;C:\Program Files (x86)\Windows Kits\10\\lib\10.0.10056.0\ucrt\x86;C:\Program Files (x86)\Windows Kits\8.1\lib\winv6.3\um\x86;'
    libpath = r'C:\WINDOWS\Microsoft.NET\Framework\v4.0.30319;C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\LIB;C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\ATLMFC\LIB;C:\Program Files (x86)\Windows Kits\8.1\References\CommonConfiguration\Neutral;\Microsoft.VCLibs\14.0\References\CommonConfiguration\neutral;'
        
    env['VSINSTALLDIR'] = installdir
    env['PATH'] = '{};{};{};{}'.format(common7ide, vcbin, common7tools, env['PATH'])
    env['VS140COMNTOOLS'] = common7tools
    env['INCLUDE'] = include 
    env['LIB'] = lib 
    env['LIBPATH'] = libpath 
    return env    


class MSVCCXXToolchain(CXXToolchain):
    def __init__(self, env=None):
        super(MSVCCXXToolchain, self).__init__()
        self.add_tool('.s', MSVCCompilerDriver(env=env))
        self.add_tool('.c', MSVCCompilerDriver(env=env))
        self.add_tool('.cc', MSVCCompilerDriver(cxx=True, env=env))
        self.add_tool('.cpp', MSVCCompilerDriver(cxx=True, env=env))
        self.archiver = MSVCArchiverDriver(env=env)
        self.linker = MSVCLinkerDriver(env=env)


class GNUCXXToolchain(CXXToolchain):
    def __init__(self):
        super(GNUCXXToolchain, self).__init__()
        self.add_tool('.S', GNUCompilerDriver(cxx=False, executable='gcc'))
        self.add_tool('.c', GNUCompilerDriver(cxx=False, executable='gcc'))
        self.add_tool('.cc', GNUCompilerDriver(cxx=True, executable='g++'))
        self.add_tool('.cpp', GNUCompilerDriver(cxx=True, executable='g++'))
        self.archiver = GNUArchiverDriver()
        self.linker = GNULinkerDriver(cxx=True, executable='g++')


class ClangCXXToolchain(CXXToolchain):
    def __init__(self):
        super(ClangCXXToolchain, self).__init__()
        self.add_tool('.S', GNUCompilerDriver(cxx=False, executable='clang'))
        self.add_tool('.c', GNUCompilerDriver(cxx=False, executable='clang'))
        self.add_tool('.cc', GNUCompilerDriver(cxx=True, executable='clang++'))
        self.add_tool('.cpp', GNUCompilerDriver(cxx=True, executable='clang++'))
        self.archiver = GNUArchiverDriver()
        self.linker = GNULinkerDriver(cxx=True, executable='clang++')
