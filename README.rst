=======================
PAM - Pun At Make
=======================

PAM is a portable build tool capable of building C/C++ and C# projects, either through its own build engine or by utilizing third party tools such as MSBuild, Xcode and Make. Projects are defined in Python scripts.

First Project
---------------

A simple Hello World project may look like this: 
::
  from build.model import CXXExecutable

  # Create a new C++ executable project
  hello = CXXExecutable('hello_world')

  # Add the sources we want to compile and link
  hello.add_sources('src/hello.cpp') 

  # Build the project for Windows using MSBuild and VS2015
  hello.add_toolchain('windows-x64-msbuild-vs14')

The project definition is saved to ``pam.py`` which is loaded by default.

Building
---------
To build the project above, invoke the tool and provide the project name:
::
  $ pam hello_world

PAM will build the ``hello_world`` project using the toolchains added to it.

Second Project
--------------
Let's get real and have a closer look at the project API and what PAM is capable of. This time we're creating a library and linking it into an executable.
::
  from build.model import CXXLibrary, CXXExecutable, ToolchainGroup

  # A toolchain group is a convenient way of using the same set of toolchains in multiple projects.
  toolchains = ToolchainGroup()
  toolchains.add_toolchain('linux-x64-pam-gcc)
  toolchains.add_toolchain('macosx-x64-pam-gcc)
  toolchains.add_toolchain('windows-x64-msbuild-vs14')
  
  # Let's build a very commonly used library, zlib. 
  zlib = CXXLibrary('zlib')

  # We add sources to the project by collecting all .c files from the zlib directory.
  # Sources are automatically paired with matching tools through their file extensions. 
  # If an unconventional file extension is used, a tool may be selected explicitly
  # with the tool attribute. For example, to build as C++ use: tool='.cpp' 
  zlib.add_sources('zlib', r'.*\.c')

  # Next we add an include path so that the library's headers can be found. 
  # When the publish attribute is set to true, the path will be inherited by 
  # all projects that depend on zlib. That way downstream projects won't be 
  # affected if the path changes in the future.
  zlib.add_incpath('zlib', publish=True)

  # The library also needs a few macros set depending on the target operating 
  # system. We can selectively set macros using the filter attribute. A filter 
  # is basically a regex matched against the name of the toolchain used. 
  # For example, if building with windows-x64-msbuild-vs14, only the first macro 
  # would be set because only 'windows' matches the toolchain name.
  # Filters can also be used when adding sources, include paths and other items. 
  # We can also publish these macros to dependent projects by setting the publish 
  # attribute, but in this case there is no need to.
  zlib.add_macro('WINDOWS', filter='windows')
  zlib.add_macro('LINUX', filter='linux')
  zlib.add_macro('DARWIN', filter='macosx)

  # Add the set of toolchains we want to use to build the library.
  zlib.add_toolchain_group(toolchains)


  # Let's utilize the zlib library by building the zpipe example found in the tarball.
  zpipe = CXXExecutable('zpipe')

  # Add sources
  zpipe.add_sources('zlib/examples/zpipe.c')

  # Add a dependency to the library
  zpipe.add_dependency(zlib)

  # Add the toolchains to use
  zpipe.add_toolchain_group(toolchains)


We can now build the zpipe utility program:
::
  $ pam zpipe

PAM will automatically only use toolchains which are supported on the current host machine.

Toolchains
----------
The following builting toolchains are available:

- linux-pam-gcc
- linux-arm-pam-gcc
- linux-x64-pam-gcc
- linux-x86-pam-gcc
- macosx-pam-clang
- macosx-x64-pam-clang
- macosx-x86-pam-clang
- windows-msbuild-vs12
- windows-msbuild-vs14
- windows-store-arm-msbuild-vs12
- windows-store-arm-msbuild-vs14
- windows-store-x86-msbuild-vs12
- windows-store-x86-msbuild-vs14
- windows-x64-msbuild-vs12
- windows-x64-msbuild-vs14
- windows-x64-nmake-vs14
- windows-x64-pam-clang-vs14
- windows-x64-pam-vs12
- windows-x64-pam-vs14
- windows-x86-msbuild-vs12
- windows-x86-msbuild-vs14
- windows-x86-nmake-vs14
- windows-x86-pam-clang-vs14
- windows-x86-pam-vs12
- windows-x86-pam-vs14

Frequently Asked Questions
--------------------------

Q: How do I install it?
````````````````````````
Use pip:
::
  $ pip install -e git+https://rand_r@bitbucket.org/rand_r/build.git#egg=Package


Q: How do I add a custom compiler flag to a project?
````````````````````````````````````````````````````

You don't, compiler flags are typically toolchain attributes. You can however use project features to change the behavior of the toolchain, for example to enable C++11 support:
::
  project.add_feature('c++11') 

Q: How can I add a custom compiler flag to a toolchain?
```````````````````````````````````````````````````````

The easiest way is to create a new toolchain by extending an existing one using a ToolchainExtender. More documentation will be provided at a later date.
::
  from build.transform.toolchain import ToolchainRegistry, ToolchainExtender

Q: What types of sources are supported?
````````````````````````````````````````

There following source file extensions are recognized:

- .appxmanifest
- .c
- .cc
- .cpp
- .cxx
- .dds
- .hlsl
- .png
- .S
- .wav
- .xaml