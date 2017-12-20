from build.model import *
from externals.googletest import googletest


source_path = GitClone("stdext-path-source", "https://github.com/srand/stdext-path.git")
source_crypto = GitClone("stdext-crypto-source", "https://github.com/srand/stdext-crypto.git")

stdext_path = cxx_project(
    name = "stdext-path",
    incpaths = [("output/stdext-path-source/include", {"publish": True})],
    dependencies = [source_path]
)

stdext_path_test = cxx_executable(
    name = "stdext-path-test",
    sources = ["output/stdext-path-source/test/test.cpp"],
    dependencies = [stdext_path, googletest],
    features = ["language-c++11"]
)

stdext_crypto = cxx_library(
    name = "stdext-crypto",
    incpaths = [("output/stdext-crypto-source/include", {"publish": True})],
    sources = ["output/stdext-crypto-source/src/crypto.cpp"],
    features = ["language-c++11"],
    libraries = [("crypto", {"publish": True, "filter": "linux"})],
    dependencies = [source_crypto]
)

stdext_crypto_test = cxx_executable(
    name = "stdext-crypto-test",
    sources = ["output/stdext-crypto-source/test/test.cpp"],
    dependencies = [googletest, stdext_crypto],
    features = ["language-c++11"]
)
