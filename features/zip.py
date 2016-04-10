from build.feature import Feature
from build.model import CXXLibrary, CXXExecutable
from build.transform import msbuild
from build.utils import Dispatch, multidispatch


class ZipFeature(Feature):
    dispatch = Dispatch()
    
    def __init__(self, name):
        super(ZipFeature, self).__init__(name)

    def transform(self, project, out_project):
        pass

zip = ZipFeature("zip")
