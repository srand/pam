from build.model import CXXExecutable, CXXLibrary, GitClone


source = GitClone(
    "jsoncpp-source",
    "https://github.com/open-source-parsers/jsoncpp")

jsoncpp = CXXLibrary("jsoncpp")
jsoncpp.add_dependency(source)
jsoncpp.add_incpath("output/jsoncpp-source/include", publish=True)
jsoncpp.add_sources("output/jsoncpp-source/src/lib_json", ".*cpp$")
jsoncpp.add_macro("JSON_HAS_RVALUE_REFERENCES", publish=True)
jsoncpp.use_feature("language-c++11")

jsoncpp_test = CXXExecutable("jsoncpp-test")
jsoncpp_test.add_dependency(jsoncpp)
jsoncpp_test.add_sources("output/jsoncpp-source/src/test_lib_json", '.*cpp$')
jsoncpp_test.use_feature("language-c++11")
