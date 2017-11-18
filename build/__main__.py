##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


import argparse
import os
import sys
import re
import time
from build.transform.toolchain import ToolchainRegistry, ToolchainLoader
from build.feature import FeatureLoader
from build.model import ProjectRegistry, ProjectLoader
import build


toolchains_path = os.path.join(os.path.dirname(__file__), os.pardir, "toolchains")
features_path = os.path.join(os.path.dirname(__file__), os.pardir, "features")

# Import toolchains and features
ToolchainLoader(toolchains_path).load()
FeatureLoader(features_path).load()


def exit(msg):
    executable = os.path.basename(sys.argv[0])
    sys.exit('{}: error: {}'.format(executable, msg))


def main():
    help = '''  PAM - The Python build engine

available toolchains:
'''

    sorted_toolchains = set()
    for toolchain_name in sorted([t.name for t in ToolchainRegistry.all()]):
        help += '  {}\n'.format(toolchain_name)

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=help)
    parser.add_argument('project', nargs='+', help='name of project to build')
    parser.add_argument('-v', '--verbose', action="store_true", help='verbose output')
    parser.add_argument('-f', '--file', default='pam.py', help='project file to load (default: pam.py)')
    parser.add_argument('-t', '--toolchain', help='toolchain to use (default: all supported)')
    parser.add_argument('-i', '--inject-toolchain', help='forcibly add a toolchain to all projects')
    args = parser.parse_args()

    if args.verbose:
        build.verbose = True

    if not os.path.exists(args.file):
        exit('file not found: {}'.format(args.file))

    if args.toolchain:
        if not any([re.search(args.toolchain, t.name) for t in ToolchainRegistry.all()]):
            exit("unrecognized toolchain '{}'".format(args.toolchain))
    else:
        args.toolchain = r'.*'

    ProjectLoader(args.file).load()

    if args.inject_toolchain:
        tc = ToolchainRegistry.find(args.inject_toolchain)
        if not tc:
            exit("unrecognized toolchain '{}'".format(args.inject_toolchain))
        for project in ProjectRegistry.all():
            if hasattr(project, "add_toolchain"):
                project.add_toolchain(args.inject_toolchain)

    projects = []
    if args.project[0] == "all":
        projects = ProjectRegistry.all()
    else:
        for project in args.project:
            try:
                projects.append(ProjectRegistry.find(project))
            except ValueError as e:
                exit("error: unrecognized project: {}".format(project))

    completed = set()
    for project in projects:
        def _build(project):
            for dependency in project.dependencies:
                _build(dependency.project)
            if project.is_toolchain_agnostic and not project.toolchains:
                transform(project)
            for toolchain_name in project.toolchains:
                if not re.search(args.toolchain, toolchain_name):
                    continue
                try:
                    toolchain = ToolchainRegistry.find(toolchain_name)
                    if not toolchain.supported:
                        continue
                except ValueError as e:
                    exit("unrecognized toolchain '{}'".format(toolchain_name))

                transform(project, toolchain)

        def transform(project, toolchain=None):
            if project in completed:
                return
            completed.add(project)
            start_time = time.time()
            print('===== Checking: %s' % (project.name))
            if project.transform(toolchain):
                elapsed = time.time() - start_time
                print('===== Done: %dm %ds' % (elapsed / 60, elapsed % 60))

        if project not in completed:
            _build(project)
    print("===== Done")

if __name__ == "__main__":
    main()
