class FeatureNoop(object):
    def transform(self, project, cxx_project):
        pass


class FeatureError(object):
    def __init__(self, msg):
        self.msg = msg

    def transform(self, project, cxx_project):
        raise RuntimeError(msg)


