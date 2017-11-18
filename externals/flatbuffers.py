from build.model import CXXLibrary, CXXExecutable, GitClone


source = GitClone(
    "flatbuffers-source",
    "https://github.com/google/flatbuffers")

flatbuffers_srcs = [
    "src/code_generators.cpp",
    "src/idl_parser.cpp",
    "src/idl_gen_text.cpp",
    "src/reflection.cpp",
    "src/util.cpp"
]

flatc_srcs = [
    "src/idl_gen_cpp.cpp",
    "src/idl_gen_general.cpp",
    "src/idl_gen_go.cpp",
    "src/idl_gen_js.cpp",
    "src/idl_gen_php.cpp",
    "src/idl_gen_python.cpp",
    "src/idl_gen_fbs.cpp",
    "src/idl_gen_grpc.cpp",
    "src/idl_gen_json_schema.cpp",
    "src/flatc.cpp",
    "src/flatc_main.cpp",
    "grpc/src/compiler/cpp_generator.cc",
    "grpc/src/compiler/go_generator.cc",
]

flatbuffers = CXXLibrary("flatbuffers")
flatbuffers.add_dependency(source)
flatbuffers.add_incpath("output/flatbuffers-source/include", publish=True)
flatbuffers.add_incpath("output/flatbuffers-source")
flatbuffers.add_sources("output/flatbuffers-source", files=flatbuffers_srcs)
flatbuffers.use_feature("language-c++11")


flatc = CXXLibrary("flatc")
flatc.add_dependency(flatbuffers)
flatc.add_incpath("output/flatbuffers-source")
flatc.add_incpath("output/flatbuffers-source/grpc")
flatc.add_sources("output/flatbuffers-source/", files=flatc_srcs)
flatc.use_feature("language-c++11")
