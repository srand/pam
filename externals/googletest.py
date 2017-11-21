from build.model import cxx_library, GitClone

source = GitClone(
    "googletest-source",
    "https://github.com/google/googletest.git")


googletest = cxx_library(
    "googletest",
    sources=[
        "output/googletest-source/googletest/src/gtest-all.cc"
    ],
    incpaths=[
        "output/googletest-source/googletest/",
        ("output/googletest-source/googletest/include", {"publish": True})
    ],
    libraries=[
        ("pthread", {"filter": "linux", "publish": True})
    ],
    dependencies=[
        source
    ]
)

googlemock = cxx_library(
    "googlemock",
    sources=[
        "output/googletest-source/googlemock/src/gmock-all.cc"
    ],
    incpaths=[
        "output/googletest-source/googlemock/",
        ("output/googletest-source/googlemock/include", {"publish": True})
    ],
    libraries=[
        ("pthread", {"filter": "linux", "publish": True})
    ],
    dependencies=[
        source,
        googletest
    ]
)
