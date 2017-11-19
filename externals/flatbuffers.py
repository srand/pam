from build.model import CXXLibrary, CXXExecutable, GitClone, Source
from build.tools import Tool, ToolRegistry
from build.transform import pybuild, msbuild
from build.tools.directory import PyBuildDirectoryCreator
import os


class ProtobufCompiler(Tool):
    def __init__(self, *args, **kwargs):
        super(ProtobufCompiler, self).__init__(*args, **kwargs)
        self._output_ext = ".h"

    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)

    def _product(self, cxx_project, source_file):
        b,e = os.path.splitext(source_file)
        return '{}_generated{}'.format(b, self._output_ext, output=cxx_project.output)

    def _cmdline(self, cxx_project, source_file):
        incdirs = cxx_project.project.get_incpaths(cxx_project.toolchain, True)
        return "flatc --cpp -o {} {} -b {}".format(
            os.path.dirname(self._product(cxx_project, source_file)),
            " ".join(set(["-I {}".format(dir.path) for dir in incdirs])),
            source_file)

    def _info(self, source_file):
        return ' [FLATC] {}'.format(source_file)

    def transform_pybuild(self, cxx_project, source_file):
        product = self._product(cxx_project, source_file.path)
        dir = self._directory(cxx_project, os.path.dirname(product))
        cxx_project.add_source(source_file.path)
        cxx_project.add_command(product, self._cmdline(cxx_project, source_file.path), self._info(source_file.path))
        cxx_project.add_dependency(product, source_file.path)
        cxx_project.add_dependency(product, dir.product)

    def transform_msbuild(self, cxx_project, sources):
        generated_srcs = []
        ig = cxx_project.create_item_group()
        for source_file in sources:
            product = self._product(cxx_project, source_file.path)
            ig.add_command(
                product,
                self._cmdline(cxx_project, source_file.path),
                source_file.path)
            generated_srcs.append(Source(product))

    def transform_msbuild_filter(self, cxx_project, sources):
        return self.transform_msbuild(cxx_project, sources)

    def transform(self, cxx_project, source_file):
        if isinstance(cxx_project, pybuild.CXXProject):
            return self.transform_pybuild(cxx_project, source_file)
        if isinstance(cxx_project, msbuild.CXXProject):
            return self.transform_msbuild(cxx_project, source_file)
        if isinstance(cxx_project, msbuild.FilterProject):
            return self.transform_msbuild_filter(cxx_project, source_file)
        raise RuntimeError("flatbuffers not supported in this toolchain")


ToolRegistry.add(".fbs", ProtobufCompiler())


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


flatc = CXXExecutable("flatc")
flatc.add_dependency(flatbuffers)
flatc.add_incpath("output/flatbuffers-source")
flatc.add_incpath("output/flatbuffers-source/grpc")
flatc.add_sources("output/flatbuffers-source/", files=flatc_srcs)
flatc.use_feature("language-c++11")


example = CXXExecutable("flatbuffers-example")
example.add_dependency(flatc)
example.add_sources("output/flatbuffers-source/samples/monster.fbs")
example.add_sources("output/flatbuffers-source/samples/sample_binary.cpp")
example.use_feature("language-c++11")
