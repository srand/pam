from build.feature import Feature
from build.model import CXXLibrary, CXXExecutable
from build.transform import msbuild
from build.utils import Dispatch, multidispatch


class ZipFeature(Feature):
    dispatch = Dispatch()
    
    def __init__(self):
        super(ZipFeature, self).__init__()

    def transform(self, project, out_project, **kwargs):
        pass

zip = ZipFeature()
