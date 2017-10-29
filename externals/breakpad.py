from build.model import CXXExecutable, CXXLibrary, GitClone, SourceGroup

source = GitClone(
    "breakpad-source",
    "https://chromium.googlesource.com/breakpad/breakpad.git")

source_lss = GitClone(
    "breakpad-lss-source",
    "https://chromium.googlesource.com/linux-syscall-support",
    "third_party/lss")

breakpad_client_srclist = [
    "src/client/linux/crash_generation/crash_generation_client.cc"
    ,"src/client/linux/crash_generation/crash_generation_server.cc"
    ,"src/client/linux/dump_writer_common/thread_info.cc"
    ,"src/client/linux/dump_writer_common/ucontext_reader.cc"
    ,"src/client/linux/handler/exception_handler.cc"
    ,"src/client/linux/handler/minidump_descriptor.cc"
    ,"src/client/linux/log/log.cc"
    ,"src/client/linux/microdump_writer/microdump_writer.cc"
    ,"src/client/linux/minidump_writer/linux_core_dumper.cc"
    ,"src/client/linux/minidump_writer/linux_dumper.cc"
    ,"src/client/linux/minidump_writer/linux_ptrace_dumper.cc"
    ,"src/client/linux/minidump_writer/minidump_writer.cc"
    ,"src/client/minidump_file_writer.cc"
    ,"src/common/convert_UTF.c"
    ,"src/common/string_conversion.cc"
    ,"src/common/linux/elf_core_dump.cc"
    ,"src/common/linux/elfutils.cc"
    ,"src/common/linux/file_id.cc"
    ,"src/common/linux/guid_creator.cc"
    ,"src/common/linux/linux_libc_support.cc"
    ,"src/common/linux/memory_mapped_file.cc"
    ,"src/common/linux/safe_readlink.cc"
    ,"src/common/android/breakpad_getcontext.S"
]

breakpad_client_linux_srcgrp = SourceGroup()
"""
for srcfile in breakpad_client_srclist:
    breakpad_client_linux_srcgrp.add_sources(
        "output/breakpad-source/{}".format(srcfile), filter="linux")
"""
breakpad_client_linux_srcgrp.add_sources(
    "output/breakpad-source/src/processor", "(?!.*unittest.cc$)(.*\.(cc|c|S)$)", filter="linux")
breakpad_client_linux_srcgrp.add_sources(
    "output/breakpad-source/src/client", "(?!.*test.cc$)(.*\.(cc|c|S)$)", filter="linux")
breakpad_client_linux_srcgrp.add_sources(
    "output/breakpad-source/src/client/linux", "(?!.*test.cc$)(.*\.(cc|c|S)$)", filter="linux", recurse=True)
breakpad_client_linux_srcgrp.add_sources(
    "output/breakpad-source/src/common", "(?!.*unittest.cc$)(.*\.(cc|c|S)$)", filter="linux")
breakpad_client_linux_srcgrp.add_sources(
    "output/breakpad-source/src/common/linux", "(?!.*test.cc$)(.*\.(cc|c|S)$)", filter="linux")

breakpad_client = CXXLibrary("breakpad_client")
breakpad_client.add_dependency(source)
breakpad_client.add_dependency(source_lss)
breakpad_client.add_incpath("output/breakpad-source/src", publish=True)
breakpad_client.add_incpath("output/breakpad-lss-source", publish=True)
breakpad_client.add_source_group(breakpad_client_linux_srcgrp)
breakpad_client.use_feature("language-c++11")
breakpad_client.add_macro("HAVE_A_OUT_H", filter="linux")

core2md = CXXExecutable("core2md")
core2md.add_dependency(source)
core2md.add_dependency(source_lss)
core2md.add_dependency(breakpad_client)
core2md.use_feature("language-c++11")
core2md.add_sources("output/breakpad-source/src/tools/linux/core2md/core2md.cc", filter="linux")

md2core = CXXExecutable("md2core")
md2core.add_dependency(source)
md2core.add_dependency(source_lss)
md2core.add_incpath("output/breakpad-source/src", publish=True)
md2core.add_incpath("output/breakpad-lss-source", publish=True)
md2core.use_feature("language-c++11")
md2core.add_sources("output/breakpad-source/src/tools/linux/md2core/minidump-2-core.cc", filter="linux")
md2core.add_sources("output/breakpad-source/src/common/linux/memory_mapped_file.cc", filter="linux")
md2core.add_sources("output/breakpad-source/src/common/path_helper.cc", filter="linux")

dump_syms = CXXExecutable("dump_syms")
dump_syms.add_dependency(source)
dump_syms.add_dependency(source_lss)
dump_syms.add_incpath("output/breakpad-source/src", publish=True)
dump_syms.add_incpath("output/breakpad-lss-source", publish=True)
dump_syms.use_feature("language-c++11")
dump_syms_linux_srclst = [
    "src/common/dwarf_cfi_to_module.cc"
    ,"src/common/dwarf_cu_to_module.cc"
    ,"src/common/dwarf_line_to_module.cc" 
    ,"src/common/language.cc"
    ,"src/common/module.cc"
    ,"src/common/path_helper.cc"
    ,"src/common/stabs_reader.cc"
    ,"src/common/stabs_to_module.cc"
    ,"src/common/dwarf/bytereader.cc"
    ,"src/common/dwarf/dwarf2diehandler.cc"
    ,"src/common/dwarf/dwarf2reader.cc"
    ,"src/common/dwarf/elf_reader.cc"
    ,"src/common/linux/crc32.cc"
    ,"src/common/linux/dump_symbols.cc"
    ,"src/common/linux/elf_symbols_to_module.cc"
    ,"src/common/linux/elfutils.cc"
    ,"src/common/linux/file_id.cc"
    ,"src/common/linux/linux_libc_support.cc"
    ,"src/common/linux/memory_mapped_file.cc"
    ,"src/common/linux/safe_readlink.cc"
    ,"src/tools/linux/dump_syms/dump_syms.cc"]
dump_syms_linux_srcgrp = SourceGroup()
for srcfile in dump_syms_linux_srclst:
    dump_syms_linux_srcgrp.add_sources("output/breakpad-source/{}".format(srcfile), filter="linux")
dump_syms.add_source_group(dump_syms_linux_srcgrp)
dump_syms.add_macro("HAVE_A_OUT_H", filter="linux")

minidump_upload = CXXExecutable("minidump_upload")
minidump_upload.add_dependency(source)
minidump_upload.add_incpath("output/breakpad-source/src", publish=True)
minidump_upload.use_feature("language-c++11")
minidump_upload.add_sources("output/breakpad-source/src/common/linux/http_upload.cc", filter="linux")
minidump_upload.add_sources("output/breakpad-source/src/tools/linux/symupload/minidump_upload.cc", filter="linux")
minidump_upload.add_library("dl", filter="linux")

sym_upload = CXXExecutable("sym_upload")
sym_upload.add_dependency(source)
sym_upload.add_incpath("output/breakpad-source/src", publish=True)
sym_upload.use_feature("language-c++11")
sym_upload.add_sources("output/breakpad-source/src/common/linux/http_upload.cc", filter="linux")
sym_upload.add_sources("output/breakpad-source/src/common/linux/symbol_upload.cc", filter="linux")
sym_upload.add_sources("output/breakpad-source/src/tools/linux/symupload/sym_upload.cc", filter="linux")
sym_upload.add_library("dl", filter="linux")
