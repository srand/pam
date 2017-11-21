from build.model import cxx_library, cxx_executable, GitClone, Source
from build.tools import Tool, ToolRegistry
from build.transform import pybuild, msbuild
from build.tools.directory import PyBuildDirectoryCreator
import os


class FlatbufferCompiler(Tool):
    def __init__(self, *args, **kwargs):
        super(FlatbufferCompiler, self).__init__(*args, **kwargs)
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


ToolRegistry.add(".fbs", FlatbufferCompiler())


source = GitClone(
    "flatbuffers-source",
    "https://github.com/google/flatbuffers")

flatbuffers_srcs = [
]

flatbuffers = cxx_library(
    "flatbuffers",
    sources=[
        "output/flatbuffers-source/src/code_generators.cpp",
        "output/flatbuffers-source/src/idl_parser.cpp",
        "output/flatbuffers-source/src/idl_gen_text.cpp",
        "output/flatbuffers-source/src/reflection.cpp",
        "output/flatbuffers-source/src/util.cpp"
    ],
    incpaths=[
        "output/flatbuffers-source",
        ("output/flatbuffers-source/include", {"publish": True})
    ],
    dependencies=[
        source
    ],
    features=[
        "language-c++11"
    ]
)

flatc = cxx_executable(
    "flatc",
    sources=[
        "output/flatbuffers-source/src/idl_gen_cpp.cpp",
        "output/flatbuffers-source/src/idl_gen_general.cpp",
        "output/flatbuffers-source/src/idl_gen_go.cpp",
        "output/flatbuffers-source/src/idl_gen_js.cpp",
        "output/flatbuffers-source/src/idl_gen_php.cpp",
        "output/flatbuffers-source/src/idl_gen_python.cpp",
        "output/flatbuffers-source/src/idl_gen_fbs.cpp",
        "output/flatbuffers-source/src/idl_gen_grpc.cpp",
        "output/flatbuffers-source/src/idl_gen_json_schema.cpp",
        "output/flatbuffers-source/src/flatc.cpp",
        "output/flatbuffers-source/src/flatc_main.cpp",
        "output/flatbuffers-source/grpc/src/compiler/cpp_generator.cc",
        "output/flatbuffers-source/grpc/src/compiler/go_generator.cc",
    ],
    incpaths=[
        "output/flatbuffers-source",
        "output/flatbuffers-source/grpc"
    ],
    dependencies=[
        source,
        flatbuffers
    ],
    features=[
        "language-c++11"
    ]
)

example = cxx_executable(
    "flatbuffers-example",
    sources=[
        "output/flatbuffers-source/samples/monster.fbs",
        ("output/flatbuffers-source/samples/sample_binary.cpp", {
            "dependencies": [
                "output/flatbuffers-source/samples/monster_generated.h"
            ]
        })
    ],
    dependencies=[
        source,
        flatc
    ],
    features=[
        "language-c++11"
    ]
)
