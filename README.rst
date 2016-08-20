=======================
PAM - Powerful And Mean
=======================

PAM is a powerful build tool capable of building C/C++ and C# projects, either natively through its own build engine or by utilizing third party Tools such as MSBuild, Xcode and Make. Projects are defined in Python scripts.

Example Project
---------------

A simple Hello World project may look like this: 
::
  from build.model import CXXExecutable

  # Create a new C++ executable project
  hello = CXXExecutable('hello_world')

  # Add the sources we want to compile and link, in this case all .cpp files from the src/ folder
  hello.add_sources('src', '.*cpp') 

  # Tell PAM how to build the project by adding a toolchain
  hello.add_toolchain('windows-x64-msbuild-vs14')  # Build for Windows using MSBuild and VS 2015
  hello.add_toolchain('linux-x64-pybuild-gcc')  # Build for Linux using internal build engine and GCC


Building
---------
To build the project above, invoke the tool and provide the project name 
::
  $ pam hello_world

By default, PAM will load projects from a file called pam.py, 
but you can of course specify a different filename by using the -f flag.