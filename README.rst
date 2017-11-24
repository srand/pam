=======================
PAM - Pun At Make
=======================

PAM is a portable build tool capable of building C/C++ projects, either through its own build engine or by utilizing third party tools such as MSBuild (Visual Studio), Xcode and Make. Projects are defined in Python scripts. 

A key differentiator for PAM is the abstraction and removal of traditional toolchain attributes from projects. In PAM, the toolchain is in fact a project attribute in its own right. This enables a single 
project to be built using multiple toolchains in different configurations. For example, a project can be built for x86, ARM and MIPS simultaneously, in 32- and 64-bit, debug and release configurations. It's all up to you.

Installing
----------
Make sure you have Python 2.7 and pip installed. Then:
::
  $ pip install -e git+https://bitbucket.org/rand_r/pam.git#egg=Package


First Project
---------------

A simple Hello World project may look like this: 
::
  from build.model import cxx_executable

  # Create a new C++ executable project
  hello = cxx_executable(
    name = "hello_world",
    sources = ["src/hello.cpp"],                # Add the sources we want to compile and link
    toolchains = ["windows-x64-msbuild-vs14"]   # Build the project for Windows using MSBuild and VS2015
  )

The project definition is saved to ``pam.py`` which is loaded by default.

Building
---------
To build the project above, invoke the tool and provide the project name:
::
  $ pam hello_world

PAM will build the ``hello_world`` project using the toolchains added to it.

Second Project
--------------
Let's get real and have a closer look at the project API and what PAM is capable of. This time we're creating a library and linking it into an executable. Of the two different APIs presented, the first one is recommended to new users. If something is unclear, skip ahead and read the comments in the old API's example. 
::
  from build.model import *
  
  toolchains = [
    "windows-x64-msbuild-vs15",
    "linux-x64-pam-gcc".
    "macosx-x64-pam-clang"
  ]
  
  features = [
    { "name": "optimize", "level": "full" },
    "language-c++11"
  ]
  
  hello = cxx_library(
    name = "hello",
    sources = ["src"],
    incpaths = [ ("include", {"publish": True}) ],
    macros = [
      ("WINDOWS", {"filter": "windows"}),
      ("LINUX", {"filter": "linux"}),
      ("MACOSX", {"filter": "macosx"}),
    ],
    features = features,
    toolchains = toolchains
  )
  
  hello_test = cxx_executable(
    name = "hello_test",
    sources = ["test"],
    dependencies = [googletest, hello],
    features = features,
    toolchains = toolchains
  )
  
  map(googletest.add_toolchain, toolchains)
  
The above code can also be written like this:  
::
  from build.model import *
  from externals.googletest import googletest
  
  # A toolchain set is a convenient way of using the same set of 
  # toolchains in multiple projects. A commonly used toolchain
  # is added for each supported platform.
  toolchains = ToolchainGroup()
  toolchains.add_toolchain("windows-x64-msbuild-vs15")
  toolchains.add_toolchain("linux-x64-pam-gcc")
  toolchains.add_toolchain("macosx-x64-pam-clang")
  
  # Similarly, use a shared set of features for all projects
  features = FeatureGroup()
  # We are compiling c++11 code
  features.use_feature("language-c++11")
  # and want optimized code
  features.use_feature("optimize", level="full")
  
  # Build a hello world library
  hello_lib = CXXLibrary("hello")
  
  # Collect and compile all files in the "src" directory.
  # Sources are automatically paired with matching tools through 
  # their file extensions. If an unconventional file extension is used,
  # a tool may be selected explicitly with the tool attribute.
  # For example, to build C code as C++, add: tool='.cpp'
  hello_lib.add_sources("src")
  
  # Next we add an include path so that the library's headers can be found. 
  # When the publish attribute is set to true, the path will be inherited by 
  # all projects that depend on 'hello'. That way downstream projects won't be 
  # affected if the path changes in the future.
  hello_lib.add_incpath("include", publish=True)
  
  # The library also needs a few macros set depending on the target operating 
  # system. We can selectively set macros using the filter attribute. A filter 
  # is basically a regex matched against the name of the toolchain used. 
  # For example, if building with windows-x64-msbuild-vs14, only the first 
  # macro would be set because only 'windows' matches the toolchain name.
  # Filters can also be used when adding sources, include paths and other 
  # items. We can also publish these macros to dependent projects by setting 
  # the publish attribute, but in this case there is no need to.
  hello_lib.add_macro("WINDOWS", filter="windows")
  hello_lib.add_macro("LINUX", filter="linux")
  hello_lib.add_macro("MACOSX", filter="macosx")
  
  # Add the set of features we want to enable for the library.
  hello_lib.add_feature_group(features)
  
  # Add the set of toolchains we want to use to build the library.
  hello_lib.add_toolchain_group(toolchains)
  
  
  # Build a test executable
  hello_test = CXXExecutable("hello_test")
  # It depends on the hello library 
  hello_test.add_dependency(hello_lib)
  
  # ... and GoogleTest which is an external and imported project.
  # PAM has builtin recepies for googletest and will download and
  # build the library source automatically.
  hello_test.add_dependency(googletest)
  
  # Add test source code
  hello_test.add_sources("test")
  
  # And our features and toolchains
  hello_test.add_feature_group(features)
  hello_test.add_toolchain_group(toolchains)
  
  # Also add our toolchains to googletest.
  googletest.add_toolchain_group(toolchains)


This project is availble as an example in the repository. To build it, run:
::
  $ cd examples/hello && pam hello_test

PAM will automatically select the toolchain supported on your current host machine.

Custom Toolchain in a Project
-----------------------------

To extend / create new toolchains:
::
  from build.model import *
  from toolchains.pam import *

  # Explicit 32-bit toolchain
  pam_gnu_toolchain(
    "linux-x86-pam-gcc",
    inherits="linux-pam-gcc",
    cflags="-m32",
    cxxflags="-m32",
    linkflags="-m32"
  )

  # Cross compile for ARM
  pam_gnu_toolchain(
    "linux-arm-pam-gcc",
    prefix="arm-linux-gnueabi-"
  )

  # Enable RTTI for MSVC
  pam_msvc_toolchain(
    "windows-x64-pam-vs15-rtti",
    inherits='windows-x64-pam-vs15',
    cxxflags="/GR",
  )

  hello = cxx_executable(
    name = "hello",
    sources = ["hello.cpp"],
    toolchains = [
      "linux-x86-pam-gcc",
      "linux-arm-pam-gcc",
      "windows-x64-pam-vs15-rtti"
    ]
  )
  
Importing External Projects
---------------------------

Pam provides build definitions for commonly used third-party libraries, for example:

- gtest
- gmock
- flatbuffers
- protobuf
- lua
- pugixml
- tinyxml
- cppjson
- zlib
- sdl

To use an external dependency in your project, simply import it.
::
  from build.model import *
  from externals.protobuf import *
  
  my_library = cxx_library(
    name = "my_library",
    sources = [
      "my_protobuf.proto"
    ],
    dependencies = [protobuf, protoc]
  )
  
By importing the externals.protobuf module, the .proto file extension will be registered
and recognized by all toolchains. During build, the my_protobuf.proto source file is 
first passed to the protoc compiler and the generated C++ source is subsequently 
automatically compiled by the selected toolchain. If you add protoc as a dependency 
to your project, the protoc compiler will also be built using the selected toolchain,
It will be automatically used to compile your profobuffers. If your project doesn't
depend on protoc, the executable must exist in your path.

Similarly, you may add support for flatbuffers (.fbs) in your build definition by 
importing the externals.flatbuffers module.

Toolchains
----------
The following builtin toolchains are available:

- linux-pam-gcc
- linux-make-gcc
- macosx-pam-clang
- macosx-make-clang
- windows-msbuild-vs12
- windows-msbuild-vs14
- windows-store-arm-msbuild-vs12
- windows-store-arm-msbuild-vs14
- windows-store-x86-msbuild-vs12
- windows-store-x86-msbuild-vs14
- windows-x64-msbuild-vs12
- windows-x64-msbuild-vs14
- windows-x64-msbuild-vs15
- windows-x64-pam-clang-vs14
- windows-x64-pam-vs12
- windows-x64-pam-vs14
- windows-x64-pam-vs15
- windows-x86-msbuild-vs12
- windows-x86-msbuild-vs14
- windows-x86-msbuild-vs15
- windows-x86-pam-clang-vs14
- windows-x86-pam-vs12
- windows-x86-pam-vs14
- windows-x86-pam-vs14

Frequently Asked Questions
--------------------------

Q: How do I add a custom compiler flag to a project?
````````````````````````````````````````````````````

You don't, compiler flags are typically toolchain attributes. You can however use project features to change the behavior of the toolchain, for example to enable C++11 support:
::
  project.use_feature('language-c++11') 

Q: How can I add a custom compiler flag to a toolchain?
```````````````````````````````````````````````````````

The easiest way is to create a new toolchain by extending an existing one using a ToolchainExtender. 
The flag is then added to the new toolchain by registering a feature. 
::
  from build.transform.toolchain import ToolchainExtender
  from build.feature import PyBuildCustomCXXFlag

  # Create a new toolchain called 'linux-x86-pam-gcc-sanitized', inheriting 'linux-x86-pam-gcc'
  extented_toolchain = ToolchainExtender('linux-x86-pam-gcc-sanitized', 'linux-x86-pam-gcc')
  
  # Add an optinal feature to the new extended toolchain. 
  # The feature is selected by calling .use_feature('sanitize-alignment') API on a project. 
  extented_toolchain.add_feature(PyBuildCustomCXXFlag('-fsanitize=alignment'), 'sanitize-alignment')    

  # Unconditional features can be added by omitting the name. Such features are used by all projects.
  extented_toolchain.add_feature(PyBuildCustomCXXFlag('-fsanitize=address'))
  
Extending MSBuild projects with new features is more difficult since we need to manupulate an XML DOM 
rather than command line arguments. You need to know a bit about MSBuild schemas.  
::
  from build.transform.toolchain import ToolchainExtender
  from build.feature import Feature
  
  # Create a new toolchain called 'windows-x86-msbuild-vs14-extended'
  extented_toolchain = ToolchainExtender('windows-x86-msbuild-vs14-extended', 'windows-x86-msbuild-vs14')    

  class MSBuildTypeInfoFeature(object):
    def transform(self, project, out_project, **kwargs):
      # A feature transforms a project from one format into another.
      # You can collect data from the input 'project' as needed. However, most 
      # features will typically only manipulate the 'out_project' to enable different 
      # compiler options.
       
      # Let's enable RTTI by setting the appropriate XML-tag in the ClCompile task definition.
      out_project.clcompile.runtimetypeinfo = "true"

  # Add an instance of our new feature to our new toolchain.
  # RTTI is now enabled in all projects using this toolchain.
  extented_toolchain.add_feature(MSBuildTypeInfoFeature())
  
  
Q: What about debug/release configurations in MSBuild projects? 
```````````````````````````````````````````````````````````````

They are not supported. You will only see a 'Default' configuration matching the toolchain used. 
If you want to build your project in different configurations you should use multiple different 
toolchains. You can easily achieve this by extending toolchains. 
::
  # Create two new toolchains, one for debug builds and another for release builds.
  debug_toolchain = ToolchainExtender('windows-x86-msbuild-vs14-debug', 'windows-x86-msbuild-vs14')
  debug_toolchain.use_feature('optimize', level='disabled')

  release_toolchain = ToolchainExtender('windows-x86-msbuild-vs14-release', 'windows-x86-msbuild-vs14')    
  release_toolchain.use_feature('optimize', level='full')
  
  project = CXXExecutable('myapp')
  project.add_toolchain('windows-x86-msbuild-vs14-debug')
  project.add_toolchain('windows-x86-msbuild-vs14-release')


Q: What types of sources are supported?
````````````````````````````````````````

There following source file extensions are recognized:

- .appxmanifest
- .c
- .cc
- .cpp
- .cxx
- .dds
- .fbs          (Google Flatbuffers: import externals.flatbuffer)
- .hlsl
- .png
- .proto        (Google Protobuf: import externals.protobuf)
- .S
- .wav
- .xaml


Q: What features are supported?
```````````````````````````````

- optimize - with mandatory argument 'level' set to one of 'disabled', 'size', 'speed', 'full'.
- language-c89 - compile as C89 code
- language-c99 - compile as C99 code
- language-c11 - compile as C11 code
- language-c++11 - compile as C++11 code
- language-c++14 - compile as C++14 code
