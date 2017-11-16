from build.model import CXXExecutable, CXXLibrary, GitClone

source = GitClone(
    "lua-source",
    "https://github.com/lua/lua")

lua = CXXLibrary("lua")
lua.add_dependency(source)
lua.add_incpath("output/lua-source", publish=True)
lua.add_sources("output/lua-source", ".*\.c$")
