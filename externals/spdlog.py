from build.model import cxx_executable, cxx_project, GitClone

source = GitClone(
    "spdlog-source",
    "https://github.com/gabime/spdlog.git")

spdlog = cxx_project(
    "spdlog",
    incpaths=[
        ("output/spdlog-source/include", {"publish": True})
    ],
    libraries=[
        ("pthread", {"filter": "linux", "publish": True})
    ],
    dependencies=[
        source
    ]
)

spdlog_test = cxx_executable(
    "spdlog-test",
    sources=[
        ("output/spdlog-source/tests", {"regex": '.*cpp$'})
    ],
    features=[
        "language-c++11"
    ],
    dependencies=[
        source,
        spdlog
    ]
)
