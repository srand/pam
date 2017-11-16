from build.model import CXXExecutable, CXXLibrary, GitClone

source = GitClone(
    "pugixml-source",
    "https://github.com/zeux/pugixml")

pugixml = CXXLibrary("pugixml")
pugixml.add_dependency(source)
pugixml.add_incpath("output/pugixml-source/src", publish=True)
pugixml.add_sources("output/pugixml-source/src/pugixml.cpp")

pugixml_test = CXXExecutable("pugixml-test")
pugixml_test.add_dependency(pugixml)
pugixml_test.add_sources("output/pugixml-source/tests", ".*test_.*cpp$")
pugixml_test.add_sources("output/pugixml-source/tests/allocator.cpp")
pugixml_test.add_sources("output/pugixml-source/tests/main.cpp")
pugixml_test.add_sources("output/pugixml-source/tests/test.cpp")
pugixml_test.add_sources("output/pugixml-source/tests/writer_string.cpp")
