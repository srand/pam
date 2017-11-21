from build.model import cxx_executable, cxx_library, GitClone

source = GitClone(
    "pugixml-source",
    "https://github.com/zeux/pugixml")

pugixml = cxx_library(
    "pugixml",
    sources=[
        "output/pugixml-source/src/pugixml.cpp"
    ],
    incpaths=[
        ("output/pugixml-source/src", {"publish": True})
    ],
    dependencies=[source]
)

pugixml_test = cxx_executable(
    "pugixml-test",
    sources=[
        ("output/pugixml-source/tests", {"regex": ".*test_.*cpp$"}),
        "output/pugixml-source/tests/allocator.cpp",
        "output/pugixml-source/tests/main.cpp",
        "output/pugixml-source/tests/test.cpp",
        "output/pugixml-source/tests/writer_string.cpp",
    ],
    dependencies=[source, pugixml]
)
