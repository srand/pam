import tempfile
import os
import re
import subprocess
from copy import copy


class Transformer(object):
    def __init__(self):
        super(Transformer, self).__init__()

    def transform(self):
        path = 'build_output' #tempfile.mkdtemp()
        self.transform_into(path)

    def transform_into(self, path):
        pass


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
            self._toolchain = template_settings._toolchain
        else:
            self._defines = set()
            self._incpaths = set()
            self._libpaths = set()
            self._cflags = []
            self._cxxflags = []
            self._linkflags = []
            self._libraries = []
            self._toolchain = None

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

    @property
    def toolchain(self):
        if not self._toolchain:
            raise RuntimeError('no toolchain assigned to settings')
        return self._toolchain

    @toolchain.setter
    def toolchain(self, toolchain):
        self._toolchain = toolchain
        
        
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
        return Command(self._product(source_file), self._cmdline(settings, source_file), self._info(source_file), env=self._env)


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
        return Command(self._product(executable), self._cmdline(settings, executable, object_files), self._info(executable), env=self._env)


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
        return Command(self._product(name), self._cmdline(name, object_files), self._info(name), env=self._env)


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
        return Command(self._product(source_file), self._cmdline(settings, source_file), self._info(source_file))


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
        return Command(self._product(executable), self._cmdline(settings, executable, object_files), self._info(executable))


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
        return Command(self._product(name), self._cmdline(name, object_files), self._info(name))


class Toolchain(object):
    def __init__(self, settings=Settings()):
        super(Toolchain, self).__init__()
        self._tools = {}
        self._settings = settings
        self._settings.toolchain = self

    @property
    def settings(self):
        return self._settings

    def add_tool(self, extension, driver):
        self._tools[extension] = driver

    def get_tool(self, extension):
        if extension not in self._tools:
            raise RuntimeError('could not find tool for {} extension'.format(extension))
        return self._tools[extension]


class CXXToolchain(Toolchain):
    def __init__(self, settings=Settings()):
        super(CXXToolchain, self).__init__()
        self._cxx_archiver = None
        self._cxx_linker = None
        
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


class MSVCCXXToolchain(CXXToolchain):
    def __init__(self, settings=Settings(), env=None):
        super(MSVCCXXToolchain, self).__init__(settings)
        self.add_tool('.s', MSVCCompilerDriver(env=env))
        self.add_tool('.c', MSVCCompilerDriver(env=env))
        self.add_tool('.cc', MSVCCompilerDriver(cxx=True, env=env))
        self.add_tool('.cpp', MSVCCompilerDriver(cxx=True, env=env))
        self.archiver = MSVCArchiverDriver(env=env)
        self.linker = MSVCLinkerDriver(env=env)


class GNUCXXToolchain(CXXToolchain):
    def __init__(self, settings=Settings()):
        super(GNUCXXToolchain, self).__init__(settings)
        self.add_tool('.S', GNUCompilerDriver(cxx=False, executable='gcc'))
        self.add_tool('.c', GNUCompilerDriver(cxx=False, executable='gcc'))
        self.add_tool('.cc', GNUCompilerDriver(cxx=True, executable='g++'))
        self.add_tool('.cpp', GNUCompilerDriver(cxx=True, executable='g++'))
        self.archiver = GNUArchiverDriver()
        self.linker = GNULinkerDriver(cxx=True, executable='g++')


class ClangCXXToolchain(CXXToolchain):
    def __init__(self, settings=Settings()):
        super(ClangCXXToolchain, self).__init__(settings)
        self.add_tool('.S', GNUCompilerDriver(cxx=False, executable='clang'))
        self.add_tool('.c', GNUCompilerDriver(cxx=False, executable='clang'))
        self.add_tool('.cc', GNUCompilerDriver(cxx=True, executable='clang++'))
        self.add_tool('.cpp', GNUCompilerDriver(cxx=True, executable='clang++'))
        self.archiver = GNUArchiverDriver()
        self.linker = GNULinkerDriver(cxx=True, executable='clang++')


def linux_x86_settings():
    toolchain = GNUCXXToolchain()
    toolchain.settings.add_cflag('-m32')
    toolchain.settings.add_cxxflag('-m32')
    toolchain.settings.add_linkflag('-m32')
    return Settings(toolchain.settings)

def mac_x86_libcxx_settings():
    toolchain = ClangCXXToolchain()
    toolchain.settings.add_cflag('-m32')
    toolchain.settings.add_cxxflag('-m32')
    toolchain.settings.add_cxxflag('-stdlib=libc++')
    toolchain.settings.add_linkflag('-m32')
    toolchain.settings.add_linkflag('-stdlib=libc++')
    return Settings(toolchain.settings)


def ios_x86_libcxx_settings():
    toolchain = ClangCXXToolchain()
    toolchain.settings.add_cflag('-m32')
    toolchain.settings.add_cxxflag('-m32')
    toolchain.settings.add_cxxflag('-stdlib=libc++')
    toolchain.settings.add_linkflag('-m32')
    toolchain.settings.add_linkflag('-stdlib=libc++')

    toolchain.settings.add_cflag('-isysroot')
    toolchain.settings.add_cflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    toolchain.settings.add_cxxflag('-isysroot')
    toolchain.settings.add_cxxflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    toolchain.settings.add_linkflag('-isysroot')
    toolchain.settings.add_linkflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    return Settings(toolchain.settings)


def ios_armv7_libcxx_settings():
    toolchain = ClangCXXToolchain()

    # Building for ARMv7
    toolchain.settings.add_cflag('-arch', 'armv7')
    toolchain.settings.add_cxxflag('-arch', 'armv7')
    toolchain.settings.add_linkflag('-arch', 'armv7')

    # With libc++
    toolchain.settings.add_cxxflag('-stdlib=libc++')
    toolchain.settings.add_linkflag('-stdlib=libc++')

    # And default iOS SDK
    toolchain.settings.add_cflag('-isysroot')
    toolchain.settings.add_cflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    toolchain.settings.add_cxxflag('-isysroot')
    toolchain.settings.add_cxxflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    toolchain.settings.add_linkflag('-isysroot')
    toolchain.settings.add_linkflag('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk')
    return Settings(toolchain.settings)


def win_x86_vs2015xp_settings():
    def create_env():
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
    
    toolchain = MSVCCXXToolchain(create_env())
    return Settings(toolchain.settings)



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
        p = subprocess.Popen(self.cmdline, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, env=self._env)
        s = iter(p.stdout.readline, b'')
        p.wait()
        for line in s: print line.strip()
        if p.returncode != 0: raise RuntimeError('job failed')
        self._completed = True


class BaseTransformer(Transformer):
    def __init__(self):
        super(BaseTransformer, self).__init__()
        self._jobs = {}
        self._tools = {}

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

    def transform_into(self, path):
        self.transform_prepare(path)
        for product in self._jobs:
            job = self._jobs[product]
            if job.required:
                job.execute()


# C/C++ transformer
class CCXXTransformer(BaseTransformer):
    def __init__(self, settings=Settings()):
        super(CCXXTransformer, self).__init__()
        self._source_regex = []
        self._source_files = []
        self._object_files = []
        self._settings = Settings(settings)

    @property
    def settings(self):
        return self._settings

    def add_incpath(self, path):
        self.settings.add_incpath(path)

    def add_define(self, key, value=None):
        self.settings.add_define(key, value)

    def add_sources(self, path, regex=r'.*', recurse=False):
        self._source_regex.append((path, regex, recurse))

    def _expand_source_path(self, path, regex, recurse):
        if os.path.isdir(path):
            if recurse:
                all_files = [os.path.join(base, file) for base, dirs, files in os.walk(path) for file in files]
            else:
                all_files = os.listdir(path)
                all_files = [os.path.join(path, file) for file in all_files]
        else:
            all_files = [path]
        matching_files = [file for file in all_files if re.match(regex, file)]

        for source_file in matching_files:
            root, ext = os.path.splitext(source_file)
            driver = self.settings.toolchain.get_tool(ext)
            job = driver.prepare(self._settings, source_file)

            self.add_job(Source(source_file))
            self.add_job(job)
            self.add_dependency(job.product, source_file)

            self._source_files.append(source_file)
            self._object_files.append(job)

    def transform_prepare(self, path):
        for path, regex, recurse in self._source_regex:
            self._expand_source_path(path, regex, recurse)


class Library(CCXXTransformer):
    def __init__(self, name, settings=Settings()):
        super(Library, self).__init__(settings)
        self._name = name
        
    @property
    def name(self):
        return self._name

    def transform_prepare(self, path):
        super(Library, self).transform_prepare(path)

        driver = self.settings.toolchain.archiver
        object_files = [object.product for object in self._object_files]
        job = driver.prepare(self.settings, self._name, object_files)
        self.add_job(job)
        for object in object_files:
            self.add_dependency(job.product, object)
        

class Executable(CCXXTransformer):
    def __init__(self, name, settings=Settings()):
        super(Executable, self).__init__(settings)
        self._name = name

    @property
    def name(self):
        return self._name

    def add_library(self, lib):
        self.settings.add_library(os.path.basename(lib.name))
        self.settings.add_libpath(os.path.dirname(lib.name))

    def transform_prepare(self, path):
        super(Executable, self).transform_prepare(path)

        object_files = [object.product for object in self._object_files]
        driver = self.settings.toolchain.linker
        job = driver.prepare(self.settings, self._name, object_files)
        self.add_job(job)
        for object in object_files:
            self.add_dependency(job.product, object)
