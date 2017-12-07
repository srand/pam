from build.model import *
from externals.googletest import googletest


source_path = GitClone("stdext-path-source", "https://github.com/srand/stdext-path.git")

stdext_path = cxx_project(
    name = "stdext-path",
    incpaths = [("output/stdext-path-source/include", {"publish": True})],
    dependencies = [source_path]
)

stdext_path_test = cxx_executable(
    name = "stdext-path-test",
    sources = ["output/stdext-path-source/test/test.cpp"],
    dependencies = [stdext_path, googletest],
    features = ["language-c++11"]
)
