from build.model import CSLibrary, CSExecutable

lib_cs = CSLibrary("Lib")
lib_cs.add_sources("tests/hello.cs/Lib.cs")

hello_world_cs = CSExecutable("Hello")
hello_world_cs.add_sources("tests/hello.cs/Hello.cs")
hello_world_cs.add_dependency(lib_cs)
