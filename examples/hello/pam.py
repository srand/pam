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
