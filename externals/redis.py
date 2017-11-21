from build.model import cxx_executable, cxx_library, GitClone

source = GitClone(
    "hiredis-source",
    "https://github.com/redis/hiredis")

hiredis = cxx_library(
    "hiredis",
    sources=[
        ("output/hiredis-source", {"regex": "(?!.*(test|dict)\.c$)(.*\.c$)"})
    ],
    incpaths=[
        ("output/hiredis-source", {"publish": True})
    ],
    dependencies=[source]
)

hiredis_test = cxx_executable(
    "hiredis-test",
    sources=[
        "output/hiredis-source/test.c"
    ],
    dependencies=[hiredis]
)
