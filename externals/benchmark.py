from build.model import CXXLibrary, GitClone

source = GitClone(
    "benchmark-source",
    "https://github.com/google/benchmark.git")

benchmark = CXXLibrary("benchmark")
benchmark.add_dependency(source)
benchmark.add_incpath("output/benchmark-source/include", publish=True)
benchmark.add_incpath("output/benchmark-source/")
benchmark.add_sources("output/benchmark-source/src", ".*\.cc$")
benchmark.use_feature("language-c++11")
benchmark.use_feature("optimize", level="full")
benchmark.add_macro("NDEBUG")
benchmark.add_macro("HAVE_STD_REGEX")
benchmark.add_library("pthread", filter="linux", publish=True)
benchmark.add_library("shlwapi", filter="windows", publish=True)

