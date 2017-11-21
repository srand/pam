from build.model import cxx_executable, cxx_library, GitClone


source = GitClone(
    "jsoncpp-source",
    "https://github.com/open-source-parsers/jsoncpp")

jsoncpp = cxx_library(
    "jsoncpp",
    sources=[
        ("output/jsoncpp-source/src/lib_json", {"regex": ".*cpp$"})
    ],
    incpaths=[
        ("output/jsoncpp-source/include", {"publish": True})
    ],
    macros=[
        "JSON_HAS_RVALUE_REFERENCES"
    ],
    features=[
        "language-c++11"
    ],
    dependencies=[source]
)

jsoncpp_test = cxx_executable(
    "jsoncpp-test",
    sources=[
        ("output/jsoncpp-source/src/test_lib_json", {"regex": '.*cpp$'})
    ],
    features=[
        "language-c++11"
    ],
    dependencies=[
        source, 
        jsoncpp
    ]
)
