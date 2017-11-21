from build.model import GitClone, Source, cxx_library, cxx_executable
from build.transform import utils, msbuild, pybuild
from build.tools import ToolRegistry, Tool
from build.tools.directory import PyBuildDirectoryCreator
from build.utils import Dispatch, multidispatch
import os


class ProtobufCompiler(Tool):
    dispatch = Dispatch()

    def __init__(self, *args, **kwargs):
        super(ProtobufCompiler, self).__init__(*args, **kwargs)
        self._output_ext = ".pb.cc"

    def _directory(self, cxx_project, dirname):
        return PyBuildDirectoryCreator().transform(cxx_project, dirname)

    def _product(self, cxx_project, source_file):
        b,e = os.path.splitext(source_file)
        return '{output}/{}{}'.format(b, self._output_ext, output=cxx_project.output)

    def _cmdline(self, cxx_project, source_file):
        incdirs = cxx_project.project.get_incpaths(cxx_project.toolchain, True)
        return "protoc {} --proto_path={} --cpp_out={} {}".format(
            source_file,
            os.path.dirname(source_file),
            os.path.dirname(self._product(cxx_project, source_file)),
            " ".join(set(["-I {}".format(dir.path) for dir in incdirs])))

    def _info(self, source_file):
        return ' [PROTOC] {}'.format(source_file)

    def transform_pybuild(self, cxx_project, source_file):
        product = self._product(cxx_project, source_file.path)
        dir = self._directory(cxx_project, os.path.dirname(product))
        cxx_project.add_source(source_file.path)
        cxx_project.add_command(product, self._cmdline(cxx_project, source_file.path), self._info(source_file.path))
        cxx_project.add_dependency(product, source_file.path)
        cxx_project.add_dependency(product, dir.product)

        tool = cxx_project.toolchain.get_tool(".cc")
        return tool.transform(cxx_project, Source(product))

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
        tool = cxx_project.toolchain.get_tool(".cc")
        return tool.transform(cxx_project, generated_srcs)

    def transform_msbuild_filter(self, cxx_project, sources):
        return self.transform_msbuild(cxx_project, sources)

    def transform(self, cxx_project, source_file):
        if isinstance(cxx_project, pybuild.CXXProject):
            return self.transform_pybuild(cxx_project, source_file)
        if isinstance(cxx_project, msbuild.CXXProject):
            return self.transform_msbuild(cxx_project, source_file)
        if isinstance(cxx_project, msbuild.FilterProject):
            return self.transform_msbuild_filter(cxx_project, source_file)
        raise RuntimeError("protobuffers not supported in this toolchain")


ToolRegistry.add(".proto", ProtobufCompiler())

source = GitClone(
    "protobuf-source",
    "https://github.com/google/protobuf")


protobuf_lite = cxx_library(
    "protobuf_lite",
    sources=[
        "output/protobuf-source/src/google/protobuf/arena.cc",
        "output/protobuf-source/src/google/protobuf/arenastring.cc",
        "output/protobuf-source/src/google/protobuf/extension_set.cc",
        "output/protobuf-source/src/google/protobuf/generated_message_table_driven_lite.cc",
        "output/protobuf-source/src/google/protobuf/generated_message_util.cc",
        "output/protobuf-source/src/google/protobuf/io/coded_stream.cc",
        "output/protobuf-source/src/google/protobuf/io/zero_copy_stream.cc",
        "output/protobuf-source/src/google/protobuf/io/zero_copy_stream_impl_lite.cc",
        "output/protobuf-source/src/google/protobuf/message_lite.cc",
        "output/protobuf-source/src/google/protobuf/repeated_field.cc",
        "output/protobuf-source/src/google/protobuf/stubs/atomicops_internals_x86_gcc.cc",
        "output/protobuf-source/src/google/protobuf/stubs/atomicops_internals_x86_msvc.cc",
        "output/protobuf-source/src/google/protobuf/stubs/bytestream.cc",
        "output/protobuf-source/src/google/protobuf/stubs/common.cc",
        "output/protobuf-source/src/google/protobuf/stubs/int128.cc",
        "output/protobuf-source/src/google/protobuf/stubs/io_win32.cc",
        "output/protobuf-source/src/google/protobuf/stubs/once.cc",
        "output/protobuf-source/src/google/protobuf/stubs/status.cc",
        "output/protobuf-source/src/google/protobuf/stubs/statusor.cc",
        "output/protobuf-source/src/google/protobuf/stubs/stringpiece.cc",
        "output/protobuf-source/src/google/protobuf/stubs/stringprintf.cc",
        "output/protobuf-source/src/google/protobuf/stubs/structurally_valid.cc",
        "output/protobuf-source/src/google/protobuf/stubs/strutil.cc",
        "output/protobuf-source/src/google/protobuf/stubs/time.cc",
        "output/protobuf-source/src/google/protobuf/wire_format_lite.cc",
    ],
    incpaths=[
        ("output/protobuf-source/src", {"publish": True})
    ],
    macros=[
        "HAVE_PTHREAD",
    ],
    dependencies=[
        source
    ]
)

protobuf = cxx_library(
    "protobuf",
    sources=[
        "output/protobuf-source/src/google/protobuf/any.cc",
        "output/protobuf-source/src/google/protobuf/any.pb.cc",
        "output/protobuf-source/src/google/protobuf/api.pb.cc",
        "output/protobuf-source/src/google/protobuf/compiler/importer.cc",
        "output/protobuf-source/src/google/protobuf/compiler/parser.cc",
        "output/protobuf-source/src/google/protobuf/descriptor.cc",
        "output/protobuf-source/src/google/protobuf/descriptor.pb.cc",
        "output/protobuf-source/src/google/protobuf/descriptor_database.cc",
        "output/protobuf-source/src/google/protobuf/duration.pb.cc",
        "output/protobuf-source/src/google/protobuf/dynamic_message.cc",
        "output/protobuf-source/src/google/protobuf/empty.pb.cc",
        "output/protobuf-source/src/google/protobuf/extension_set_heavy.cc",
        "output/protobuf-source/src/google/protobuf/field_mask.pb.cc",
        "output/protobuf-source/src/google/protobuf/generated_message_reflection.cc",
        "output/protobuf-source/src/google/protobuf/generated_message_table_driven.cc",
        "output/protobuf-source/src/google/protobuf/io/gzip_stream.cc",
        "output/protobuf-source/src/google/protobuf/io/printer.cc",
        "output/protobuf-source/src/google/protobuf/io/strtod.cc",
        "output/protobuf-source/src/google/protobuf/io/tokenizer.cc",
        "output/protobuf-source/src/google/protobuf/io/zero_copy_stream_impl.cc",
        "output/protobuf-source/src/google/protobuf/map_field.cc",
        "output/protobuf-source/src/google/protobuf/message.cc",
        "output/protobuf-source/src/google/protobuf/reflection_ops.cc",
        "output/protobuf-source/src/google/protobuf/service.cc",
        "output/protobuf-source/src/google/protobuf/source_context.pb.cc",
        "output/protobuf-source/src/google/protobuf/struct.pb.cc",
        "output/protobuf-source/src/google/protobuf/stubs/mathlimits.cc",
        "output/protobuf-source/src/google/protobuf/stubs/substitute.cc",
        "output/protobuf-source/src/google/protobuf/text_format.cc",
        "output/protobuf-source/src/google/protobuf/timestamp.pb.cc",
        "output/protobuf-source/src/google/protobuf/type.pb.cc",
        "output/protobuf-source/src/google/protobuf/unknown_field_set.cc",
        "output/protobuf-source/src/google/protobuf/util/delimited_message_util.cc",
        "output/protobuf-source/src/google/protobuf/util/field_comparator.cc",
        "output/protobuf-source/src/google/protobuf/util/field_mask_util.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/datapiece.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/default_value_objectwriter.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/error_listener.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/field_mask_utility.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/json_escaping.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/json_objectwriter.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/json_stream_parser.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/object_writer.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/proto_writer.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/protostream_objectsource.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/protostream_objectwriter.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/type_info.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/type_info_test_helper.cc",
        "output/protobuf-source/src/google/protobuf/util/internal/utility.cc",
        "output/protobuf-source/src/google/protobuf/util/json_util.cc",
        "output/protobuf-source/src/google/protobuf/util/message_differencer.cc",
        "output/protobuf-source/src/google/protobuf/util/time_util.cc",
        "output/protobuf-source/src/google/protobuf/util/type_resolver_util.cc",
        "output/protobuf-source/src/google/protobuf/wire_format.cc",
        "output/protobuf-source/src/google/protobuf/wrappers.pb.cc",
    ],
    incpaths=[
        ("output/protobuf-source/src", {"publish": True})
    ],
    dependencies=[
        source, 
        protobuf_lite
    ]
)

js_embed = cxx_executable(
    "js_embed",
    sources=[
        "output/protobuf-source/src/google/protobuf/compiler/js/embed.cc"
    ]
)

protoc_lib = cxx_library(
    "protoc_lib",
    sources=[
        "output/protobuf-source/src/google/protobuf/compiler/code_generator.cc",
        "output/protobuf-source/src/google/protobuf/compiler/command_line_interface.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_enum.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_enum_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_extension.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_file.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_generator.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_helpers.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_map_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_message.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_message_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_padding_optimizer.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_primitive_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_service.cc",
        "output/protobuf-source/src/google/protobuf/compiler/cpp/cpp_string_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_doc_comment.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_enum.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_enum_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_field_base.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_generator.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_helpers.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_map_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_message.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_message_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_primitive_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_reflection_class.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_repeated_enum_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_repeated_message_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_repeated_primitive_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_source_generator_base.cc",
        "output/protobuf-source/src/google/protobuf/compiler/csharp/csharp_wrapper_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_context.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_doc_comment.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_enum.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_enum_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_enum_field_lite.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_enum_lite.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_extension.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_extension_lite.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_file.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_generator.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_generator_factory.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_helpers.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_lazy_message_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_lazy_message_field_lite.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_map_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_map_field_lite.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_message.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_message_builder.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_message_builder_lite.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_message_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_message_field_lite.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_message_lite.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_name_resolver.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_primitive_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_primitive_field_lite.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_service.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_shared_code_generator.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_string_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/java/java_string_field_lite.cc",
        "output/protobuf-source/src/google/protobuf/compiler/javanano/javanano_enum.cc",
        "output/protobuf-source/src/google/protobuf/compiler/javanano/javanano_enum_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/javanano/javanano_extension.cc",
        "output/protobuf-source/src/google/protobuf/compiler/javanano/javanano_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/javanano/javanano_file.cc",
        "output/protobuf-source/src/google/protobuf/compiler/javanano/javanano_generator.cc",
        "output/protobuf-source/src/google/protobuf/compiler/javanano/javanano_helpers.cc",
        "output/protobuf-source/src/google/protobuf/compiler/javanano/javanano_map_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/javanano/javanano_message.cc",
        "output/protobuf-source/src/google/protobuf/compiler/javanano/javanano_message_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/javanano/javanano_primitive_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/js/js_generator.cc",
        "output/protobuf-source/src/google/protobuf/compiler/js/well_known_types_embed.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_enum.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_enum_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_extension.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_file.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_generator.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_helpers.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_map_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_message.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_message_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_oneof.cc",
        "output/protobuf-source/src/google/protobuf/compiler/objectivec/objectivec_primitive_field.cc",
        "output/protobuf-source/src/google/protobuf/compiler/php/php_generator.cc",
        "output/protobuf-source/src/google/protobuf/compiler/plugin.cc",
        "output/protobuf-source/src/google/protobuf/compiler/plugin.pb.cc",
        "output/protobuf-source/src/google/protobuf/compiler/python/python_generator.cc",
        "output/protobuf-source/src/google/protobuf/compiler/ruby/ruby_generator.cc",
        "output/protobuf-source/src/google/protobuf/compiler/subprocess.cc",
        "output/protobuf-source/src/google/protobuf/compiler/zip_writer.cc"
    ],
    commands=[
        {
            "command": "js_embed {inputs} > {output}",
            "output": "output/protobuf-source/src/google/protobuf/compiler/js/well_known_types_embed.cc",
            "inputs": [
                "output/protobuf-source/src/google/protobuf/compiler/js/well_known_types/any.js",
                "output/protobuf-source/src/google/protobuf/compiler/js/well_known_types/struct.js",
                "output/protobuf-source/src/google/protobuf/compiler/js/well_known_types/timestamp.js",
            ]
        },
    ],
    incpaths=[
        ("output/protobuf-source/src", { "publish": True })
    ],
    dependencies=[
        source,
        protobuf
    ]
)

protoc = cxx_executable(
    "protoc",
    sources=["output/protobuf-source/src/google/protobuf/compiler/main.cc"],
    dependencies=[protoc_lib]
)

example = cxx_library(
    "protobuf-addressbook",
    sources=["output/protobuf-source/examples/addressbook.proto"],
    dependencies=[protoc]
)
