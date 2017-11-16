from build.model import CXXExecutable, CXXLibrary, GitClone

source = GitClone(
    "hiredis-source",
    "https://github.com/redis/hiredis")

hiredis = CXXLibrary("hiredis")
hiredis.add_dependency(source)
hiredis.add_incpath("output/hiredis-source", publish=True)
hiredis.add_sources("output/hiredis-source", "(?!.*(test|dict)\.c$)(.*\.c$)")

hiredis_test = CXXExecutable("hiredis-test")
hiredis_test.add_dependency(hiredis)
hiredis_test.add_sources("output/hiredis-source/test.c")
