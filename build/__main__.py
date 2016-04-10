import os
import sys
from build.transform.toolchain import ToolchainRegistry, ToolchainLoader
from build.feature import FeatureLoader
from build.model import ProjectRegistry, ProjectLoader

toolchains_path = os.path.join(os.path.dirname(__file__), os.pardir, "toolchains")
features_path = os.path.join(os.path.dirname(__file__), os.pardir, "features")
projects_path = os.path.join(os.path.dirname(__file__), os.pardir, "projects")

# Import toolchains, features and projects
ToolchainLoader(toolchains_path).load()
FeatureLoader(features_path).load()
ProjectLoader(projects_path).load()


def main():
    toolchain_name = sys.argv[1]
    project_name = sys.argv[2]
    
    try:
        toolchain = ToolchainRegistry.find(toolchain_name)
    except ValueError as e:
        print("error: unrecognized toolchain '{}'".format(toolchain_name))
        sys.exit(-1)
        
    try:
        project = ProjectRegistry.find(project_name)
    except ValueError as e:
        print("error: unrecognized project: {}".format(project_name))
        sys.exit(-1)
        
    project.transform(toolchain)
    
if __name__ == "__main__":
    main()
