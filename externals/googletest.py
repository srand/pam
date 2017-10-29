from build.model import CXXLibrary, GitClone

source = GitClone(
    "googletest-source",
    "https://github.com/google/googletest.git")

googletest = CXXLibrary("googletest")
googletest.add_dependency(source)
googletest.add_incpath("output/googletest-source/googletest/include", publish=True)
googletest.add_incpath("output/googletest-source/googletest/")
googletest.add_sources("output/googletest-source/googletest/src/gtest-all.cc")
googletest.add_library("pthread", filter="linux", publish=True)

googlemock = CXXLibrary("googlemock")
googlemock.add_dependency(source)
googlemock.add_dependency(googletest)
googlemock.add_incpath("output/googletest-source/googlemock/include", publish=True)
googlemock.add_incpath("output/googletest-source/googlemock/")
googlemock.add_sources("output/googletest-source/googlemock/src/gmock-all.cc")
