from build.model import cxx_library, GitClone

source = GitClone(
    "benchmark-source",
    "https://github.com/google/benchmark.git")

benchmark = cxx_library(
    "benchmark",
    sources=[
        ("output/benchmark-source/src", {"regex": ".*\.cc$"})
    ],
    incpaths=[
        "output/benchmark-source/",
        ("output/benchmark-source/include", {"publish": True})
    ],
    features=[
        "language-c++11",
        ("optimize", {"level": "full"})
    ],
    macros=[
        "NDEBUG",
        "HAVE_STD_REGEX"
    ],
    libraries=[
        ("pthread", {"filter": "linux", "publish": True}),
        ("shlwapi", {"filter": "windows", "publish": True})
    ],
    dependencies=[
        source
    ]
)

