import argparse
import os
import sys
import re
from build.transform.toolchain import ToolchainRegistry, ToolchainLoader
from build.feature import FeatureLoader
from build.model import ProjectRegistry, ProjectLoader

toolchains_path = os.path.join(os.path.dirname(__file__), os.pardir, "toolchains")
features_path = os.path.join(os.path.dirname(__file__), os.pardir, "features")

# Import toolchains and features
ToolchainLoader(toolchains_path).load()
FeatureLoader(features_path).load()


def exit(msg):
    executable = os.path.basename(sys.argv[0])
    sys.exit('{}: error: {}'.format(executable, msg))


def main():
    parser = argparse.ArgumentParser(description='Python build')
    parser.add_argument('project', nargs='+', help='name of project to build')
    parser.add_argument('-f', '--file', default='pam.py', help='project file to load (default: pam.py)')
    parser.add_argument('-t', '--toolchain', help='toolchain to use (default: all supported)')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        exit('file not found: {}'.format(args.file))

    if args.toolchain:
        try:
            ToolchainRegistry.find(args.toolchain)
        except ValueError as e:
            exit("unrecognized toolchain '{}'".format(args.toolchain))
    else:
        args.toolchain = r'.*'

    ProjectLoader(args.file).load()

    projects = []
    for project in args.project:
        try:
            projects.append(ProjectRegistry.find(project))
        except ValueError as e:
            exit("error: unrecognized project: {}".format(project))

    completed = set()
    for project in projects:
        def build(project):
            completed.add(project)
            for toolchain_name in project.toolchains:
                for dependency in project.dependencies:
                    if dependency not in completed:
                        build(dependency)
                if not re.search(args.toolchain, toolchain_name):
                    continue
                try:
                    toolchain = ToolchainRegistry.find(toolchain_name)
                except ValueError as e:
                    exit("unrecognized toolchain '{}'".format(toolchain_name))
                project.transform(toolchain)
        if project not in completed:
            build(project)


if __name__ == "__main__":
    main()
