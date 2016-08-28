from build.model import CXXLibrary, CXXExecutable, ToolchainGroup

# A toolchain group is a convenient way of using the same set of toolchains in multiple projects.
toolchains = ToolchainGroup()
toolchains.add_toolchain('linux-x64-pam-gcc')
toolchains.add_toolchain('macosx-x64-pam-clang')
toolchains.add_toolchain('windows-x86-pam-vs14')
toolchains.add_toolchain('windows-x64-pam-vs14')
toolchains.add_toolchain('windows-x64-msbuild-vs14')
  
# Let's build a very commonly used library, zlib. 
zlib = CXXLibrary('zlib')

# We add sources to the project by collecting all .c files from the zlib directory.
# Sources are automatically paired with matching tools through their file extensions. 
# If an unconventional file extension is used, a tool may be selected explicitly
# with the tool attribute. For example, to build as C++ use: tool='.cpp' 
zlib.add_sources('zlib', r'.*\.c$')

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
zlib.add_macro('DARWIN', filter='macosx')

# Compile code according to ANSI C89
zlib.use_feature('language-c89')

# Optimize the generated code 
zlib.use_feature('optimize', level='full')

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
