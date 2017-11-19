##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


class Tool(object):
    def __init__(self):
        pass

    def transform(project, out_project, sources):
        pass


class ToolRegistry(object):
    _tools = {}

    @staticmethod
    def add(extension, driver):
        ToolRegistry._tools[extension] = driver

    @staticmethod
    def find(extension):
        if extension not in ToolRegistry._tools:
            return None
        return ToolRegistry._tools[extension]

    @staticmethod
    def all():
        return ToolRegistry._tools.values()
