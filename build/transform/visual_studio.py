from copy import copy
from os import path, environ
from _winreg import HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, OpenKey, QueryValueEx


def _ReadKey(root, key, sub_key):
    value = ''
    try:
        with OpenKey(root, key) as regkey:
            value, _ = QueryValueEx(regkey, sub_key)
    except:
        pass
    return str(value)


def _ReadKeys(keylist):
    for (root, key, sub_key) in keylist:
        value = _ReadKey(root, key, sub_key)
        if value: return value
    return ''


def _GetVSCommonToolsDir(version):
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\VisualStudio\SxS\VS7', version),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\VisualStudio\SxS\VS7', version),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VS7', version),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VS7', version)])


def _GetWindowsSdkDir():
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Microsoft SDKs\Windows\v8.1', 'InstallationFolder'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\Microsoft SDKs\Windows\v8.1', 'InstallationFolder'),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\Microsoft SDKs\Windows\v8.1', 'InstallationFolder'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\Microsoft SDKs\Windows\v8.1', 'InstallationFolder')])

    
def _GetExtensionSdkDir(env):
    manifest = "Microsoft SDKs\Windows\v8.1\ExtensionSDKs\Microsoft.VCLibs\14.0\SDKManifest.xml"
    if env.get("ProgramFiles") and path.exists(path.join(env["ProgramFiles"], manifest)):
        return path.join(env["ProgramFiles"], 'Microsoft SDKs\Windows\v8.1\ExtensionSDKs')
    if env.get("ProgramFiles(x86)") and path.exists(path.join(env["ProgramFiles(x86)"], manifest)):
        return path.join(env["ProgramFiles(x86)"], 'Microsoft SDKs\Windows\v8.1\ExtensionSDKs')
    return ''


def _GetWindowsSdkExecutablePath32():
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Microsoft SDKs\Windows\v8.1A\WinSDK-NetFx40Tools', 'InstallationFolder'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\Microsoft SDKs\Windows\v8.1A\WinSDK-NetFx40Tools', 'InstallationFolder'),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\Microsoft SDKs\Windows\v8.1A\WinSDK-NetFx40Tools', 'InstallationFolder'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\Microsoft SDKs\Windows\v8.1A\WinSDK-NetFx40Tools', 'InstallationFolder')])


def _GetWindowsSdkExecutablePath64():
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Microsoft SDKs\Windows\v8.1A\WinSDK-NetFx40Tools-x64', 'InstallationFolder'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\Microsoft SDKs\Windows\v8.1A\WinSDK-NetFx40Tools-x64', 'InstallationFolder'),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\Microsoft SDKs\Windows\v8.1A\WinSDK-NetFx40Tools-x64', 'InstallationFolder'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\Microsoft SDKs\Windows\v8.1A\WinSDK-NetFx40Tools-x64', 'InstallationFolder')])


def _GetVSInstallDir(version):
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\VisualStudio\SxS\VS7', version),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\VisualStudio\SxS\VS7', version),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VS7', version),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VS7', version)])


def _GetVCInstallDir(version):
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\VisualStudio\SxS\VC7', version),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\VisualStudio\SxS\VC7', version),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VC7', version),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VC7', version)])


def _GetFSharpInstallDir():
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\VisualStudio\14.0\Setup\F#', 'ProductDir'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\VisualStudio\14.0\Setup\F#', 'ProductDir'),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\14.0\Setup\F#', 'ProductDir'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\14.0\Setup\F#', 'ProductDir')])


def _GetUniversalCRTSdkDir():
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows Kits\Installed Roots', 'KitsRoot10'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\Windows Kits\Installed Roots', 'KitsRoot10'),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\Windows Kits\Installed Roots', 'KitsRoot10'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\Windows Kits\Installed Roots', 'KitsRoot10')])


def _GetFrameworkDir32():
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\VisualStudio\SxS\VC7', 'FrameworkDir32'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\VisualStudio\SxS\VC7', 'FrameworkDir32'),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VC7', 'FrameworkDir32'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VC7', 'FrameworkDir32')])


def _GetFrameworkDir64():
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\VisualStudio\SxS\VC7', 'FrameworkDir64'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\VisualStudio\SxS\VC7', 'FrameworkDir64'),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VC7', 'FrameworkDir64'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VC7', 'FrameworkDir64')])


def _GetFrameworkVer32():
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\VisualStudio\SxS\VC7', 'FrameworkVer32'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\VisualStudio\SxS\VC7', 'FrameworkVer32'),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VC7', 'FrameworkVer32'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VC7', 'FrameworkVer32')])


def _GetFrameworkVer64():
    return _ReadKeys([
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\VisualStudio\SxS\VC7', 'FrameworkVer64'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Microsoft\VisualStudio\SxS\VC7', 'FrameworkVer64'),
        (HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VC7', 'FrameworkVer64'),
        (HKEY_CURRENT_USER,  r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VC7', 'FrameworkVer64')])


def _AppendEnv(env, var, value):
    env[var] = "{};{}".format(value, _SafeEnv(env, var))


def _AppendEnvIfExists(env, var, value):
    if path.exists(value):
        env[var] = "{};{}".format(value, _SafeEnv(env, var))


def _SafeEnv(env, var):
    return env[var] if env.get(var) else ''


def VCVars(version, target="x86", host="x86", store=False):
    env = {}
    for key in environ:
        env[key] = environ.get(key)
    
    env['VS140COMNTOOLS'] = _GetVSCommonToolsDir(version)
    env['Framework40Version'] = 'v4.0'
    env['VisualStudioVersion'] = version
    env['WindowsSdkDir'] = _GetWindowsSdkDir() 
    env['ExtensionSdkDir'] = _GetExtensionSdkDir(env)
    env['WindowsSDK_ExecutablePath_x86'] = _GetWindowsSdkExecutablePath32()
    env['WindowsSDK_ExecutablePath_x64'] = _GetWindowsSdkExecutablePath64()
    env['VSINSTALLDIR'] = _GetVSInstallDir(version)
    env['VCINSTALLDIR'] = _GetVCInstallDir(version)
    env['FSHARPINSTALLDIR'] = _GetFSharpInstallDir()
    env['UniversalCRTSdkDir'] = _GetUniversalCRTSdkDir()
    env['FrameworkVer32'] = _GetFrameworkVer32()
    env['FrameworkVer64'] = _GetFrameworkVer64()
    env['FrameworkDir32'] = _GetFrameworkDir32()
    env['FrameworkDir64'] = _GetFrameworkDir64()
    env['Platform'] = target.upper()

    if host == "x86":
        env['FrameworkDir'] = env['FrameworkDir32']
        env['FrameworkVersion'] = env['FrameworkVer32']
        _AppendEnv(env, 'PATH', env['WindowsSDK_ExecutablePath_x86'])
        _AppendEnv(env, 'PATH', path.join(env['WindowsSdkDir'], r'bin\x86'))

    if host == "x64":
        env['FrameworkDir'] = env['FrameworkDir64']
        env['FrameworkVersion'] = env['FrameworkVer64']
        _AppendEnv(env, 'PATH', env['WindowsSDK_ExecutablePath_x64'])
        _AppendEnv(env, 'PATH', path.join(env['WindowsSdkDir'], r'bin\x86'))
        _AppendEnv(env, 'PATH', path.join(env['WindowsSdkDir'], r'bin\x64'))
                
    env['DevEnvDir'] = path.join(env['VSINSTALLDIR'], r'Common7\IDE\\')        
    _AppendEnvIfExists(env, 'PATH', path.join(env['VSINSTALLDIR'], r'Team Tools\Performance Tools'))
    if host == "x64":
        _AppendEnvIfExists(env, 'PATH', path.join(env['VSINSTALLDIR'], r'Team Tools\Performance Tools\x64'))
            
    _AppendEnvIfExists(env, 'PATH', path.join(_SafeEnv(env, 'ProgramFiles'), r'HTML Help Workshop'))
    _AppendEnvIfExists(env, 'PATH', path.join(_SafeEnv(env, 'ProgramFiles(x86)'), r'HTML Help Workshop'))
    _AppendEnvIfExists(env, 'PATH', path.join(env['VCINSTALLDIR'], r'VCPackages'))
    _AppendEnvIfExists(env, 'PATH', path.join(env['FrameworkDir'], env['Framework40Version']))
    _AppendEnvIfExists(env, 'PATH', path.join(env['FrameworkDir'], env['FrameworkVersion']))
    _AppendEnvIfExists(env, 'PATH', path.join(env['VSINSTALLDIR'], r'Common7\Tools'))
    if host == "x86":
        _AppendEnvIfExists(env, 'PATH', path.join(env['VCINSTALLDIR'], r'bin'))
    if host == "x86" and target == "x64":
        _AppendEnvIfExists(env, 'PATH', path.join(env['VCINSTALLDIR'], r'bin\x86_amd64'))
    if host == "x86" and target == "arm":
        _AppendEnvIfExists(env, 'PATH', path.join(env['VCINSTALLDIR'], r'bin\x86_arm'))
    if host == "x64":
        _AppendEnvIfExists(env, 'PATH', path.join(env['VCINSTALLDIR'], r'bin\amd64'))
    if host == "x64" and target == "x86":
        _AppendEnvIfExists(env, 'PATH', path.join(env['VCINSTALLDIR'], r'bin\amd64_x86'))
    if host == "x64" and target == "arm":
        _AppendEnvIfExists(env, 'PATH', path.join(env['VCINSTALLDIR'], r'bin\amd64_arm'))

    _AppendEnv(env, 'PATH', env['DevEnvDir'])
    if host == "x86":
        _AppendEnvIfExists(env, 'PATH', path.join(_SafeEnv(env, 'ProgramFiles'), 'MSBuild', version, 'bin'))
        _AppendEnvIfExists(env, 'PATH', path.join(_SafeEnv(env, 'ProgramFiles(x86)'), 'MSBuild', version, 'bin'))
    if host == "x64":
        _AppendEnvIfExists(env, 'PATH', path.join(_SafeEnv(env, 'ProgramFiles'), 'MSBuild', version, 'bin\amd64'))
        _AppendEnvIfExists(env, 'PATH', path.join(_SafeEnv(env, 'ProgramFiles(x86)'), 'MSBuild', version, 'bin\amd64'))
    _AppendEnvIfExists(env, 'PATH', path.join(env['VSINSTALLDIR'], r'VSTSDB\Deploy'))
    _AppendEnvIfExists(env, 'PATH', path.join(env['FSHARPINSTALLDIR']))
    _AppendEnvIfExists(env, 'PATH', path.join(env['DevEnvDir'], r'CommonExtensions\Microsoft\TestWindow'))

    _AppendEnv(env, 'INCLUDE', path.join(env['WindowsSdkDir'], r'include\shared'))
    _AppendEnv(env, 'INCLUDE', path.join(env['WindowsSdkDir'], r'include\um'))
    _AppendEnv(env, 'INCLUDE', path.join(env['WindowsSdkDir'], r'include\winrt'))
    _AppendEnv(env, 'LIBPATH', path.join(env['WindowsSdkDir'], r'References\CommonConfiguration\Neutral'))
    _AppendEnv(env, 'LIBPATH', path.join(env['ExtensionSdkDir'], 'Microsoft.VCLibs', version, r'References\CommonConfiguration\neutral'))
    _AppendEnv(env, 'LIB', path.join(env['WindowsSdkDir'], r'lib\winv6.3\um\{}'.format(target)))

    if env['UniversalCRTSdkDir']:
        _AppendEnv(env, 'INCLUDE', path.join(env['UniversalCRTSdkDir'], r'include\10.0.10056.0\ucrt'))
        _AppendEnv(env, 'LIB', path.join(env['UniversalCRTSdkDir'], r'lib\10.0.10056.0\ucrt\{}'.format(target)))

    _AppendEnvIfExists(env, 'INCLUDE', path.join(env['VCINSTALLDIR'], r'ATLMFC\INCLUDE'))
    _AppendEnvIfExists(env, 'INCLUDE', path.join(env['VCINSTALLDIR'], r'INCLUDE'))

    if store:
        if target == "x86":
            _AppendEnvIfExists(env, 'LIB', path.join(env['VCINSTALLDIR'], r'LIB\STORE'))
            _AppendEnvIfExists(env, 'LIBPATH', path.join(env['VCINSTALLDIR'], r'LIB\STORE'))
        if target == "x64":
            _AppendEnvIfExists(env, 'LIB', path.join(env['VCINSTALLDIR'], r'LIB\amd64\STORE'))
            _AppendEnvIfExists(env, 'LIBPATH', path.join(env['VCINSTALLDIR'], r'LIB\amd64\STORE'))
        if target == "arm":
            _AppendEnvIfExists(env, 'LIB', path.join(env['VCINSTALLDIR'], r'LIB\ARM\STORE'))
            _AppendEnvIfExists(env, 'LIBPATH', path.join(env['VCINSTALLDIR'], r'LIB\ARM\STORE'))
    else:
        if target == "x86":
            _AppendEnvIfExists(env, 'LIB', path.join(env['VCINSTALLDIR'], r'ATLMFC\LIB'))
            _AppendEnvIfExists(env, 'LIB', path.join(env['VCINSTALLDIR'], r'LIB'))
            _AppendEnvIfExists(env, 'LIBPATH', path.join(env['VCINSTALLDIR'], r'ATLMFC\LIB'))
            _AppendEnvIfExists(env, 'LIBPATH', path.join(env['VCINSTALLDIR'], r'LIB'))
        if target == "x64":
            _AppendEnvIfExists(env, 'LIB', path.join(env['VCINSTALLDIR'], r'ATLMFC\LIB\amd64'))
            _AppendEnvIfExists(env, 'LIB', path.join(env['VCINSTALLDIR'], r'LIB\amd64'))
            _AppendEnvIfExists(env, 'LIBPATH', path.join(env['VCINSTALLDIR'], r'ATLMFC\LIB\amd64'))
            _AppendEnvIfExists(env, 'LIBPATH', path.join(env['VCINSTALLDIR'], r'LIB\amd64'))
        if target == "arm":
            _AppendEnvIfExists(env, 'LIB', path.join(env['VCINSTALLDIR'], r'ATLMFC\LIB\ARM'))
            _AppendEnvIfExists(env, 'LIB', path.join(env['VCINSTALLDIR'], r'LIB\ARM'))
            _AppendEnvIfExists(env, 'LIBPATH', path.join(env['VCINSTALLDIR'], r'ATLMFC\LIB\ARM'))
            _AppendEnvIfExists(env, 'LIBPATH', path.join(env['VCINSTALLDIR'], r'LIB\ARM'))
    _AppendEnvIfExists(env, 'LIBPATH', path.join(env['FrameworkDir'], env['Framework40Version']))
    _AppendEnv(env, 'LIBPATH', path.join(env['FrameworkDir'], env['FrameworkVersion']))
    return env


def VS12VCVars(*args, **kwargs):
   return VCVars('12.0', *args, **kwargs) 
    

def VS14VCVars(*args, **kwargs):
   return VCVars('14.0', *args, **kwargs) 
