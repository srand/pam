from build.model import cxx_executable, cxx_library, GitClone

source = GitClone(
    "tinyxml2-source",
    "https://github.com/leethomason/tinyxml2")

tinyxml2 = cxx_library(
    "tinyxml2",
    sources=[
        "output/tinyxml2-source/tinyxml2.cpp"
    ],
    incpaths=[
        ("output/tinyxml2-source", {"publish": True})
    ],
    dependencies=[source]
)

tinyxml2_test = cxx_executable(
    "tinyxml2-test",
    sources=[
        "output/tinyxml2-source/xmltest.cpp"
    ],
    features=["language-c++11"],
    dependencies=[source, tinyxml2]
)
