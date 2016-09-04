import platform


class Requirement(object):
    def __init__(self):
        super(Requirement, self).__init__()

    @property
    def satisfied(self):
        return True


class HostRequirement(Requirement):
    def __init__(self, host):
        super(HostRequirement, self).__init__()
        self.host = host

    @property
    def satisfied(self):
        return platform.system() == self.host


HostRequirement.WINDOWS = HostRequirement('Windows')
HostRequirement.LINUX = HostRequirement('Linux')
HostRequirement.DARWIN = HostRequirement('Darwin')
