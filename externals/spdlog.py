from build.model import CXXExecutable, CXXProject, GitClone

source = GitClone(
    "spdlog-source",
    "https://github.com/gabime/spdlog.git")

spdlog = CXXProject("spdlog")
spdlog.add_dependency(source)
spdlog.add_incpath("output/spdlog-source/include", publish=True)
spdlog.add_library("pthread", filter="linux", publish=True)

spdlog_test = CXXExecutable("spdlog-test")
spdlog_test.add_dependency(spdlog)
spdlog_test.add_sources("output/spdlog-source/tests", '.*cpp$')
spdlog_test.use_feature("language-c++11")
