from build.model import CXXExecutable, CXXLibrary, GitClone, PythonProject, DependencyGroup, Source
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

    @multidispatch(dispatch, pybuild.CXXProject, Source)
    def transform(self, cxx_project, source_file):
        product = self._product(cxx_project, source_file.path)
        dir = self._directory(cxx_project, os.path.dirname(product))
        cxx_project.add_source(source_file.path)
        cxx_project.add_command(product, self._cmdline(cxx_project, source_file.path), self._info(source_file.path))
        cxx_project.add_dependency(product, source_file.path)
        cxx_project.add_dependency(product, dir.product)

        tool = cxx_project.toolchain.get_tool(".cc")
        return tool.transform(cxx_project, Source(product))

    #@multidispatch(dispatch, msbuild.CXXProject, Source)
    #def transform(self, cxx_project, source_file):
    #    pass

    @multidispatch(dispatch)
    def transform(self, cxx_project, source_file):
        raise RuntimeError("protobuffers not supported in this toolchain")


ToolRegistry.add(".proto", ProtobufCompiler())


source = GitClone(
    "protobuf-source",
    "https://github.com/google/protobuf")


protobuf_lite_srcs = [
    "src/google/protobuf/arena.cc",
    "src/google/protobuf/arenastring.cc",
    "src/google/protobuf/extension_set.cc",
    "src/google/protobuf/generated_message_table_driven_lite.cc",
    "src/google/protobuf/generated_message_util.cc",
    "src/google/protobuf/io/coded_stream.cc",
    "src/google/protobuf/io/zero_copy_stream.cc",
    "src/google/protobuf/io/zero_copy_stream_impl_lite.cc",
    "src/google/protobuf/message_lite.cc",
    "src/google/protobuf/repeated_field.cc",
    "src/google/protobuf/stubs/atomicops_internals_x86_gcc.cc",
    "src/google/protobuf/stubs/atomicops_internals_x86_msvc.cc",
    "src/google/protobuf/stubs/bytestream.cc",
    "src/google/protobuf/stubs/common.cc",
    "src/google/protobuf/stubs/int128.cc",
    "src/google/protobuf/stubs/io_win32.cc",
    "src/google/protobuf/stubs/once.cc",
    "src/google/protobuf/stubs/status.cc",
    "src/google/protobuf/stubs/statusor.cc",
    "src/google/protobuf/stubs/stringpiece.cc",
    "src/google/protobuf/stubs/stringprintf.cc",
    "src/google/protobuf/stubs/structurally_valid.cc",
    "src/google/protobuf/stubs/strutil.cc",
    "src/google/protobuf/stubs/time.cc",
    "src/google/protobuf/wire_format_lite.cc",
]
protobuf_lite = CXXLibrary("protobuf_lite")
protobuf_lite.add_dependency(source)
protobuf_lite.add_incpath("output/protobuf-source/src", publish=True)
protobuf_lite.add_sources("output/protobuf-source", files=protobuf_lite_srcs)
protobuf_lite.add_macro("HAVE_PTHREAD")


protobuf_srcs = [
    "src/google/protobuf/any.cc",
    "src/google/protobuf/any.pb.cc",
    "src/google/protobuf/api.pb.cc",
    "src/google/protobuf/compiler/importer.cc",
    "src/google/protobuf/compiler/parser.cc",
    "src/google/protobuf/descriptor.cc",
    "src/google/protobuf/descriptor.pb.cc",
    "src/google/protobuf/descriptor_database.cc",
    "src/google/protobuf/duration.pb.cc",
    "src/google/protobuf/dynamic_message.cc",
    "src/google/protobuf/empty.pb.cc",
    "src/google/protobuf/extension_set_heavy.cc",
    "src/google/protobuf/field_mask.pb.cc",
    "src/google/protobuf/generated_message_reflection.cc",
    "src/google/protobuf/generated_message_table_driven.cc",
    "src/google/protobuf/io/gzip_stream.cc",
    "src/google/protobuf/io/printer.cc",
    "src/google/protobuf/io/strtod.cc",
    "src/google/protobuf/io/tokenizer.cc",
    "src/google/protobuf/io/zero_copy_stream_impl.cc",
    "src/google/protobuf/map_field.cc",
    "src/google/protobuf/message.cc",
    "src/google/protobuf/reflection_ops.cc",
    "src/google/protobuf/service.cc",
    "src/google/protobuf/source_context.pb.cc",
    "src/google/protobuf/struct.pb.cc",
    "src/google/protobuf/stubs/mathlimits.cc",
    "src/google/protobuf/stubs/substitute.cc",
    "src/google/protobuf/text_format.cc",
    "src/google/protobuf/timestamp.pb.cc",
    "src/google/protobuf/type.pb.cc",
    "src/google/protobuf/unknown_field_set.cc",
    "src/google/protobuf/util/delimited_message_util.cc",
    "src/google/protobuf/util/field_comparator.cc",
    "src/google/protobuf/util/field_mask_util.cc",
    "src/google/protobuf/util/internal/datapiece.cc",
    "src/google/protobuf/util/internal/default_value_objectwriter.cc",
    "src/google/protobuf/util/internal/error_listener.cc",
    "src/google/protobuf/util/internal/field_mask_utility.cc",
    "src/google/protobuf/util/internal/json_escaping.cc",
    "src/google/protobuf/util/internal/json_objectwriter.cc",
    "src/google/protobuf/util/internal/json_stream_parser.cc",
    "src/google/protobuf/util/internal/object_writer.cc",
    "src/google/protobuf/util/internal/proto_writer.cc",
    "src/google/protobuf/util/internal/protostream_objectsource.cc",
    "src/google/protobuf/util/internal/protostream_objectwriter.cc",
    "src/google/protobuf/util/internal/type_info.cc",
    "src/google/protobuf/util/internal/type_info_test_helper.cc",
    "src/google/protobuf/util/internal/utility.cc",
    "src/google/protobuf/util/json_util.cc",
    "src/google/protobuf/util/message_differencer.cc",
    "src/google/protobuf/util/time_util.cc",
    "src/google/protobuf/util/type_resolver_util.cc",
    "src/google/protobuf/wire_format.cc",
    "src/google/protobuf/wrappers.pb.cc",
]
protobuf = CXXLibrary("protobuf")
protobuf.add_dependency(source)
protobuf.add_incpath("output/protobuf-source/src", publish=True)
protobuf.add_sources("output/protobuf-source/", files=protobuf_srcs)
protobuf.add_dependency(protobuf_lite)


js_embed = CXXExecutable("js_embed")
js_embed.add_sources("output/protobuf-source/src/google/protobuf/compiler/js/embed.cc")


protoc_lib_srcs = [
    "src/google/protobuf/compiler/code_generator.cc",
    "src/google/protobuf/compiler/command_line_interface.cc",
    "src/google/protobuf/compiler/cpp/cpp_enum.cc",
    "src/google/protobuf/compiler/cpp/cpp_enum_field.cc",
    "src/google/protobuf/compiler/cpp/cpp_extension.cc",
    "src/google/protobuf/compiler/cpp/cpp_field.cc",
    "src/google/protobuf/compiler/cpp/cpp_file.cc",
    "src/google/protobuf/compiler/cpp/cpp_generator.cc",
    "src/google/protobuf/compiler/cpp/cpp_helpers.cc",
    "src/google/protobuf/compiler/cpp/cpp_map_field.cc",
    "src/google/protobuf/compiler/cpp/cpp_message.cc",
    "src/google/protobuf/compiler/cpp/cpp_message_field.cc",
    "src/google/protobuf/compiler/cpp/cpp_padding_optimizer.cc",
    "src/google/protobuf/compiler/cpp/cpp_primitive_field.cc",
    "src/google/protobuf/compiler/cpp/cpp_service.cc",
    "src/google/protobuf/compiler/cpp/cpp_string_field.cc",
    "src/google/protobuf/compiler/csharp/csharp_doc_comment.cc",
    "src/google/protobuf/compiler/csharp/csharp_enum.cc",
    "src/google/protobuf/compiler/csharp/csharp_enum_field.cc",
    "src/google/protobuf/compiler/csharp/csharp_field_base.cc",
    "src/google/protobuf/compiler/csharp/csharp_generator.cc",
    "src/google/protobuf/compiler/csharp/csharp_helpers.cc",
    "src/google/protobuf/compiler/csharp/csharp_map_field.cc",
    "src/google/protobuf/compiler/csharp/csharp_message.cc",
    "src/google/protobuf/compiler/csharp/csharp_message_field.cc",
    "src/google/protobuf/compiler/csharp/csharp_primitive_field.cc",
    "src/google/protobuf/compiler/csharp/csharp_reflection_class.cc",
    "src/google/protobuf/compiler/csharp/csharp_repeated_enum_field.cc",
    "src/google/protobuf/compiler/csharp/csharp_repeated_message_field.cc",
    "src/google/protobuf/compiler/csharp/csharp_repeated_primitive_field.cc",
    "src/google/protobuf/compiler/csharp/csharp_source_generator_base.cc",
    "src/google/protobuf/compiler/csharp/csharp_wrapper_field.cc",
    "src/google/protobuf/compiler/java/java_context.cc",
    "src/google/protobuf/compiler/java/java_doc_comment.cc",
    "src/google/protobuf/compiler/java/java_enum.cc",
    "src/google/protobuf/compiler/java/java_enum_field.cc",
    "src/google/protobuf/compiler/java/java_enum_field_lite.cc",
    "src/google/protobuf/compiler/java/java_enum_lite.cc",
    "src/google/protobuf/compiler/java/java_extension.cc",
    "src/google/protobuf/compiler/java/java_extension_lite.cc",
    "src/google/protobuf/compiler/java/java_field.cc",
    "src/google/protobuf/compiler/java/java_file.cc",
    "src/google/protobuf/compiler/java/java_generator.cc",
    "src/google/protobuf/compiler/java/java_generator_factory.cc",
    "src/google/protobuf/compiler/java/java_helpers.cc",
    "src/google/protobuf/compiler/java/java_lazy_message_field.cc",
    "src/google/protobuf/compiler/java/java_lazy_message_field_lite.cc",
    "src/google/protobuf/compiler/java/java_map_field.cc",
    "src/google/protobuf/compiler/java/java_map_field_lite.cc",
    "src/google/protobuf/compiler/java/java_message.cc",
    "src/google/protobuf/compiler/java/java_message_builder.cc",
    "src/google/protobuf/compiler/java/java_message_builder_lite.cc",
    "src/google/protobuf/compiler/java/java_message_field.cc",
    "src/google/protobuf/compiler/java/java_message_field_lite.cc",
    "src/google/protobuf/compiler/java/java_message_lite.cc",
    "src/google/protobuf/compiler/java/java_name_resolver.cc",
    "src/google/protobuf/compiler/java/java_primitive_field.cc",
    "src/google/protobuf/compiler/java/java_primitive_field_lite.cc",
    "src/google/protobuf/compiler/java/java_service.cc",
    "src/google/protobuf/compiler/java/java_shared_code_generator.cc",
    "src/google/protobuf/compiler/java/java_string_field.cc",
    "src/google/protobuf/compiler/java/java_string_field_lite.cc",
    "src/google/protobuf/compiler/javanano/javanano_enum.cc",
    "src/google/protobuf/compiler/javanano/javanano_enum_field.cc",
    "src/google/protobuf/compiler/javanano/javanano_extension.cc",
    "src/google/protobuf/compiler/javanano/javanano_field.cc",
    "src/google/protobuf/compiler/javanano/javanano_file.cc",
    "src/google/protobuf/compiler/javanano/javanano_generator.cc",
    "src/google/protobuf/compiler/javanano/javanano_helpers.cc",
    "src/google/protobuf/compiler/javanano/javanano_map_field.cc",
    "src/google/protobuf/compiler/javanano/javanano_message.cc",
    "src/google/protobuf/compiler/javanano/javanano_message_field.cc",
    "src/google/protobuf/compiler/javanano/javanano_primitive_field.cc",
    "src/google/protobuf/compiler/js/js_generator.cc",
    "src/google/protobuf/compiler/js/well_known_types_embed.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_enum.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_enum_field.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_extension.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_field.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_file.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_generator.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_helpers.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_map_field.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_message.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_message_field.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_oneof.cc",
    "src/google/protobuf/compiler/objectivec/objectivec_primitive_field.cc",
    "src/google/protobuf/compiler/php/php_generator.cc",
    "src/google/protobuf/compiler/plugin.cc",
    "src/google/protobuf/compiler/plugin.pb.cc",
    "src/google/protobuf/compiler/python/python_generator.cc",
    "src/google/protobuf/compiler/ruby/ruby_generator.cc",
    "src/google/protobuf/compiler/subprocess.cc",
    "src/google/protobuf/compiler/zip_writer.cc"
]
protoc_js_srcs = [
    "output/protobuf-source/src/google/protobuf/compiler/js/well_known_types/any.js",
    "output/protobuf-source/src/google/protobuf/compiler/js/well_known_types/struct.js",
    "output/protobuf-source/src/google/protobuf/compiler/js/well_known_types/timestamp.js",
]
protoc_lib = CXXLibrary("protoc_lib")
protoc_lib.add_dependency(source)
protoc_lib.add_incpath("output/protobuf-source/src", publish=True)
protoc_lib.add_sources("output/protobuf-source/", files=protoc_lib_srcs)
protoc_lib.add_dependency(js_embed)
protoc_lib.add_dependency(protobuf)
protoc_lib.add_command(
    output="output/protobuf-source/src/google/protobuf/compiler/js/well_known_types_embed.cc",
    inputs=protoc_js_srcs,
    command="js_embed {inputs} > {output}"
)

protoc = CXXExecutable("protoc")
protoc.add_dependency(protoc_lib)
protoc.add_sources("output/protobuf-source/src/google/protobuf/compiler/main.cc")


example = CXXLibrary("protobuf-addressbook")
example.add_dependency(protoc)
example.add_sources("output/protobuf-source/examples/addressbook.proto")
