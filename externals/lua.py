from build.model import cxx_library, GitClone

source = GitClone(
    "lua-source",
    "https://github.com/lua/lua")

lua = cxx_library(
    "lua",
    sources=[
        ("output/lua-source", {"regex": ".*\.c$"})
    ],
    incpaths=[
        ("output/lua-source", {"publish": True})
    ],
    dependencies=[
        source
    ]
)
