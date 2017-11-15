from build.model import CXXExecutable, CXXLibrary, GitClone

source = GitClone(
    "tinyxml2-source",
    "https://github.com/leethomason/tinyxml2")

tinyxml2 = CXXLibrary("tinyxml2")
tinyxml2.add_dependency(source)
tinyxml2.add_incpath("output/tinyxml2-source", publish=True)
tinyxml2.add_sources("output/tinyxml2-source/tinyxml2.cpp")

tinyxml2_test = CXXExecutable("tinyxml2-test")
tinyxml2_test.add_dependency(tinyxml2)
tinyxml2_test.add_sources("output/tinyxml2-source/xmltest.cpp")
tinyxml2_test.use_feature("language-c++11")
