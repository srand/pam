##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


import platform
import os


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


class PathRequirement(Requirement):
    def __init__(self, path):
        super(PathRequirement, self).__init__()
        self.path = [path] if type(path) != list else path

    @property
    def satisfied(self):
        return any([os.path.exists(path) for path in self.path])


class EnvRequirement(Requirement):
    def __init__(self, env):
        super(EnvRequirement, self).__init__()
        self.env = env

    @property
    def satisfied(self):
        return os.getenv(self.env)
