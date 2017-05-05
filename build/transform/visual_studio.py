##############################################################################
#
# (C) 2016 - Robert Andersson - All rights reserved.
#
# This file and its contents are the property of Robert Andersson
# and may not be distributed, copied, or disclosed, in whole or in part,
# for any reason without written consent of the copyright holder.
#
##############################################################################


from copy import copy
from os import path, environ, listdir, pardir
import utils


def VCVars(version, scripts, *args, **kwargs):
    class _VCVars(object):
        def __init__(self):
            self.env = None

        def __getitem__(self, item):
            if not self.env:
                self.env = self._initialize()
            return self.env[item]

        def _initialize(self):
            for script in scripts:
                if path.exists(script):
                    rc, stdout, stderr = utils.execute('{} "{}" {}'.format(
                        path.join(__file__, pardir, "vcvars.bat"),
                        script, kwargs["arch"]), output=False)
                    if rc == 0:
                        env = eval(stdout[0])
                        env["VisualStudioVersion"] = version
                        return env
            raise RuntimeError("could not initialize the Visual Studio environment")

        def __len__(self):
            if not self.env:
                self.env = self._initialize()
            return len(self.env)

        def keys(self):
            if not self.env:
                self.env = self._initialize()
            return self.env.keys()

        def values(self):
            if not self.env:
                self.env = self._initialize()
            return self.env.values()

    return _VCVars()


def VS12VCVars(*args, **kwargs):
    scripts = [path.join(environ["VS120COMNTOOLS"], pardir, pardir, "VC", "vcvarsall.bat")] if "VS120COMNTOOLS" in environ else []
    return VCVars("12.0", scripts, *args, **kwargs)


def VS14VCVars(*args, **kwargs):
    scripts = [path.join(environ["VS140COMNTOOLS"], pardir, pardir, "VC", "vcvarsall.bat")] if "VS140COMNTOOLS" in environ else []
    return VCVars("14.0", scripts, *args, **kwargs)


def VS15VCVars(*args, **kwargs):
    scripts = [r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvarsall.bat"]
    return VCVars("15.0", scripts, *args, **kwargs)
