from build.utils import Loader


class FeatureRegistry(object):
    _features = {}
    
    @staticmethod
    def add(feature):
        # print("Registering feature: {}".format(feature.name))
        FeatureRegistry._features[feature.name] = feature
        
    @staticmethod
    def find(feature):
        if feature not in FeatureRegistry._features:
            raise ValueError(feature) 
        return FeatureRegistry._features[feature]
    

class FeatureLoader(Loader):
    def __init__(self, path):
        super(FeatureLoader, self).__init__("build.features", path)


class Feature(object):
    def __init__(self):
        super(Feature, self).__init__()

    def transform(self, project, transformed, **kwargs):
        pass
