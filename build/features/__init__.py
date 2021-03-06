##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


class FeatureNoop(object):
    def transform(self, project, cxx_project):
        pass


class FeatureError(object):
    def __init__(self, msg):
        self.msg = msg

    def transform(self, project, cxx_project, **kwargs):
        raise RuntimeError(msg)

