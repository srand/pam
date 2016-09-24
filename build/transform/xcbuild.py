from build import model
from build.transform import utils
from build.transform.toolchain import Toolchain
import random
import os


class Element(object):
    def __init__(self, reference=None, value=None):
        self.reference = reference if reference else hex(random.getrandbits(96))[2:-1]
        self.value = value
        
    def serialize(self, indent=2):
        return ' ' * indent + '{reference} = {value};\n'.format(reference=self.reference, value=self.value)


class ReferenceElement(Element):
    def __init__(self, reference=None):
        super(ReferenceElement, self).__init__(reference)
        
    def serialize(self, indent=2):
        return ' ' * indent + '{reference},\n'.format(reference=self.reference)


class StringElement(Element):
    def __init__(self, reference=None, value=None):
        super(StringElement, self).__init__(reference, value)
        
    def serialize(self, indent=2):
        return ' ' * indent + '{reference} = "{value}";\n'.format(reference=self.reference, value=self.value)


class ListElement(Element):
    def __init__(self, reference=None, quote=False):
        super(ListElement, self).__init__(reference)
        self.value = self
        self.__children = []
        self._quote = quote

    def append(self, item):
        self.__children.append(item)
   
    def extend(self, item):
        self.__children.extend(item)
        
    def serialize(self, indent=2):
        str =  ' ' * indent + '%s = (\n' % self.reference
        for reference in self.__children:
            if not self._quote:
                str += ' ' * (indent+2) + '%s,\n' % reference
            else:
                str += ' ' * (indent+2) + '"%s",\n' % reference 
        str += ' ' * indent + ');\n'
        return str


class MapElement(Element):
    def __init__(self, reference=None):
        super(MapElement, self).__init__(reference)
        self.value = self
        self.__children = []

    def append(self, item):
        self.__children.append(item)

    def serialize(self, indent=2):
        str =  ' ' * indent + '%s = {\n' % self.reference
        str += self.serialize_children(indent+2)
        str += ' ' * indent + '};\n'
        return str

    def serialize_children(self, indent=2):
        str = ''
        for child in self.__children:
            str += child.serialize(indent)
        return str


class Attribute(object):
    def __init__(self, attribute, varname=None, values=None, cls=Element, required=True):
        self.attribute = attribute
        self.varname = varname if varname is not None else attribute.lower()
        self.values = values
        self.cls = cls
        self.required = required
    
    def __call__(self, cls):
        def decorate(cls, attribute, varname, values, element_cls):
            def _check_value(value, values):
                if values and value not in values:
                    raise ValueError('{} is not one of {}'.format(value, values))

            def init(self):
                if not hasattr(self, '_'+varname):
                    e = element_cls(attribute)
                    self.append(e)            
                    setattr(self, '_'+varname, e)
                    return e

            def child_get(self):
                if not hasattr(self, '_'+varname):
                    init(self)
                return getattr(self, '_'+varname).value        
    
            def child_set(self, value):
                _check_value(value, values)
                if value is None: return
                init(self)
                getattr(self,'_'+varname).value = value

            def decorate_init(old_init):
                def __init__(self, *args, **kwargs):
                    old_init(self, *args, **kwargs)
                    init(self)
                return __init__
                
            if self.required:
                cls.__init__ = decorate_init(cls.__init__) 
            setattr(cls, varname, property(child_get, child_set))
            return cls
        return decorate(cls, self.attribute, self.varname, self.values, self.cls)


class Composition(object):
    def __init__(self, cls, name):
        self.cls = cls
        self.name = name if name is not None else attribute.lower()
    
    def __call__(self, cls):
        def decorate(cls, comp_cls, name):
            def create(self, *args, **kwargs):
                child = comp_cls(*args, **kwargs)
                self.append(child)
                return child
            setattr(cls, 'create_' + name, create)
            return cls
        return decorate(cls, self.cls, self.name)


@Attribute('productName')
@Attribute('name')
@Attribute('dependencies', cls=ListElement)
@Attribute('buildPhases', cls=ListElement)
@Attribute('buildConfigurationList')
@Attribute('isa')
class PBXAggregateTarget(MapElement):
    def __init__(self):
        super(PBXAggregateTarget, self).__init__()
        self.isa = 'PBXAggregateTarget'


@Attribute('fileRef', 'file_ref')
@Attribute('isa')
class PBXBuildFile(MapElement):
    def __init__(self):
        super(PBXBuildFile, self).__init__()
        self.isa = 'PBXBuildFile'


@Attribute('remoteInfo')
@Attribute('remoteGlobalIDString')
@Attribute('proxyType')
@Attribute('containerPortal')
@Attribute('isa')
class PBXContainerItemProxy(MapElement):
    def __init__(self):
        super(PBXContainerItemProxy, self).__init__()
        self.isa = 'PBXContainerItemProxy'


@Attribute('runOnlyForDeploymentPostprocessing')
@Attribute('files')
@Attribute('dstSubfolderSpec')
@Attribute('dstPath')
@Attribute('buildActionMask')
@Attribute('isa')
class PBXCopyFilesBuildPhase(MapElement):
    def __init__(self):
        super(PBXCopyFilesBuildPhase, self).__init__()
        self.isa = 'PBXCopyFilesBuildPhase'


@Attribute('sourceTree', 'source_tree',  required=False)
@Attribute('path', required=False)
@Attribute('name', required=False)
@Attribute('lastKnownFileType', 'last_known_file_type', required=False)
@Attribute('explicitFileType', 'explicit_file_type', required=False)
@Attribute('fileEncoding', 'file_encoding', required=False)
@Attribute('includeInIndex', 'include_in_index', required=False)
@Attribute('isa')
class PBXFileReference(MapElement):
    def __init__(self):
        super(PBXFileReference, self).__init__()
        self.isa = 'PBXFileReference'


@Attribute('runOnlyForDeploymentPostprocessing', 'run_only_for_deployment_postprocessing', required=False)
@Attribute('files', cls=ListElement)
@Attribute('buildActionMask', 'build_action_mask')
@Attribute('isa')
class PBXFrameworksBuildPhase(MapElement):
    def __init__(self):
        super(PBXFrameworksBuildPhase, self).__init__()
        self.isa = 'PBXFrameworksBuildPhase'
        self.run_only_for_deployment_postprocessing = 0
        self.build_action_mask = 2147483647


@Attribute('sourceTree', cls=StringElement)
@Attribute('name', required=False)
@Attribute('children', cls=ListElement)
@Attribute('isa')
class PBXGroup(MapElement):
    def __init__(self):
        super(PBXGroup, self).__init__()
        self.isa = 'PBXGroup'
        self.sourcetree = '<group>'


@Attribute('runOnlyForDeploymentPostprocessing', 'run_only_for_deployment_postprocessing')
@Attribute('files', cls=ListElement)
@Attribute('buildActionMask', 'build_action_mask')
@Attribute('isa')
class PBXHeadersBuildPhase(MapElement):
    def __init__(self):
        super(PBXHeadersBuildPhase, self).__init__()
        self.isa = 'PBXHeadersBuildPhase'
        self.run_only_for_deployment_postprocessing = 0
        self.build_action_mask = 2147483647


@Attribute('productType', 'product_type', cls=StringElement)
@Attribute('productReference', 'product_reference')
@Attribute('productName', 'product_name')
@Attribute('productInstallPath', 'product_install_path', required=False)
@Attribute('name')
@Attribute('dependencies', cls=ListElement, required=False)
@Attribute('buildPhases', 'build_phases', cls=ListElement)
@Attribute('buildConfigurationList', 'build_config_list', required=False)
@Attribute('isa')
class PBXNativeTarget(MapElement):
    def __init__(self):
        super(PBXNativeTarget, self).__init__()
        self.isa = 'PBXNativeTarget'


@Attribute('attributes', cls=MapElement)
@Attribute('targets', cls=ListElement)
@Attribute('projectRoot', 'project_root', cls=StringElement, required=False)
@Attribute('projectReferences', 'project_references', required=False)
@Attribute('projectDirPath', 'project_dir_path', cls=StringElement, required=False)
@Attribute('productRefGroup', 'product_ref_group', required=False)
@Attribute('mainGroup', 'main_group', required=False)
@Attribute('knownRegions', 'known_regions', cls=ListElement)
@Attribute('hasScannedForEncodings', 'has_scanned_for_encodings', required=False)
@Attribute('developmentRegion', 'development_region', required=False)
@Attribute('compatibilityVersion', 'compatibility_version', cls=StringElement, required=False)
@Attribute('buildConfigurationList', 'build_config_list', required=False)
@Attribute('isa')
class PBXProject(MapElement):
    def __init__(self):
        super(PBXProject, self).__init__()
        self.isa = 'PBXProject'
        self.project_root = ''
        self.project_dir_path = ''
        self.target_attribs = MapElement('TargetAttributes')
        self.attributes.append(self.target_attribs)
        self.attributes.append(Element('LastUpgradeCheck', '0720'))


@Attribute('runOnlyForDeploymentPostprocessing', 'run_only_for_deployment_postprocessing')
@Attribute('files', cls=ListElement)
@Attribute('buildActionMask', 'build_action_mask')
@Attribute('isa')
class PBXResourcesBuildPhase(MapElement):
    def __init__(self):
        super(PBXResourcesBuildPhase, self).__init__()
        self.isa = 'PBXResourcesBuildPhase'
        self.run_only_for_deployment_postprocessing = 0
        self.build_action_mask = 2147483647


@Attribute('shellScript', 'shell_script')
@Attribute('shellPath', 'shell_path')
@Attribute('runOnlyForDeploymentPostprocessing', 'run_only_for_deployment_postprocessing')
@Attribute('outputPaths', 'output_paths', cls=ListElement)
@Attribute('inputPaths', 'input_paths', cls=ListElement)
@Attribute('files', cls=ListElement)
@Attribute('buildActionMask', 'build_action_mask')
@Attribute('isa')
class PBXShellScriptBuildPhase(MapElement):
    def __init__(self):
        super(PBXShellScriptBuildPhase, self).__init__()
        self.isa = 'PBXShellScriptBuildPhase'
        self.run_only_for_deployment_postprocessing = 0
        self.build_action_mask = 2147483647


@Attribute('runOnlyForDeploymentPostprocessing', 'run_only_for_deployment_postprocessing')
@Attribute('files', cls=ListElement)
@Attribute('buildActionMask', 'build_action_mask')
@Attribute('isa')
class PBXSourcesBuildPhase(MapElement):
    def __init__(self):
        super(PBXSourcesBuildPhase, self).__init__()
        self.isa = 'PBXSourcesBuildPhase'
        self.run_only_for_deployment_postprocessing = 0
        self.build_action_mask = 2147483647


@Attribute('targetProxy')
@Attribute('target')
@Attribute('isa')
class PBXTargetDependency(MapElement):
    def __init__(self):
        super(PBXTargetDependency, self).__init__()
        self.isa = 'PBXTargetDependency'


@Attribute('sourceTree')
@Attribute('name')
@Attribute('children', cls=ListElement)
@Attribute('isa')
class PBXVariantGroup(MapElement):
    def __init__(self):
        super(PBXVariantGroup, self).__init__()
        self.isa = 'PBXVariantGroup'


@Attribute('name')
@Attribute('buildSettings', 'build_settings', cls=MapElement, required=True)
@Attribute('baseConfigurationReference', 'base_config_reference', required=False)
@Attribute('isa')
class XCBuildConfiguration(MapElement):
    def __init__(self):
        super(XCBuildConfiguration, self).__init__()
        self.isa = 'XCBuildConfiguration'


@Attribute('defaultConfigurationName', 'default_config_name')
@Attribute('defaultConfigurationIsVisible', 'default_config_is_visible')
@Attribute('buildConfigurations', 'build_configs', cls=ListElement)
@Attribute('isa')
class XCConfigurationList(MapElement):
    def __init__(self):
        super(XCConfigurationList, self).__init__()
        self.isa = 'XCConfigurationList'
        self.default_config_is_visible = 0


@Composition(PBXBuildFile, 'build_file')
#@Composition(PBXAppleScriptBuildPhase, 'applescriptbuildphase')  # PBXBuildPhase
@Composition(PBXCopyFilesBuildPhase, 'copyfilesbuildphase')  # PBXBuildPhase
@Composition(PBXFrameworksBuildPhase, 'frameworksbuildphase')  # PBXBuildPhase
@Composition(PBXHeadersBuildPhase, 'headersbuildphase')  # PBXBuildPhase
@Composition(PBXResourcesBuildPhase, 'resourcesbuildphase')  # PBXBuildPhase
@Composition(PBXShellScriptBuildPhase, 'shellscriptbuildphase')  # PBXBuildPhase
@Composition(PBXSourcesBuildPhase, 'sources_buildphase')  # PBXBuildPhase
@Composition(PBXContainerItemProxy, 'containeritemproxy')
@Composition(PBXFileReference, 'file_reference')  # PBXFileElement
@Composition(PBXGroup, 'group')  # PBXFileElement
@Composition(PBXVariantGroup, 'variantgroup')  # PBXFileElement
@Composition(PBXAggregateTarget, 'aggregatetarget')  # PBXTarget
#@Composition(PBXLegacyTarget, 'legacytarget')  # PBXTarget
@Composition(PBXNativeTarget, 'native_target')  # PBXTarget
@Composition(PBXProject, 'project')
@Composition(PBXTargetDependency, 'target_dependency')
@Composition(XCBuildConfiguration, 'build_config')
@Composition(XCConfigurationList, 'config_list')
class ObjectMapElement(MapElement):
    def __init__(self, id):
        super(ObjectMapElement, self).__init__(id)


@Attribute('rootObject', 'root_object')
@Attribute('objects', cls=ObjectMapElement)
@Attribute('objectVersion', 'object_version')
@Attribute('classes', cls=MapElement)
@Attribute('archiveVersion', 'archive_version')
class RootElement(MapElement):
    def __init__(self):
        super(RootElement, self).__init__('')
            
    def serialize(self, indent=2):
        str = '// !$*UTF8*$!\n'
        str += '{\n'
        str += self.serialize_children(indent)
        str += '}\n'
        return str


class CXXProject(RootElement):
    FILE_TYPE_H = 'sourcecode.c.h'
    FILE_TYPE_C = 'sourcecode.c.c'
    FILE_TYPE_CPP = 'sourcecode.cpp.cpp'
    FILE_TYPE_ARCHIVE = 'archive.ar'

    def __init__(self, toolchain, name):
        super(CXXProject, self).__init__()
        self.name = name
        self.output = os.path.join(toolchain.attributes.output, self.name)
        self.archive_version = 1
        self.object_version = 46
                
        config_list, config = self.create_config_list('Default')
        config.build_settings.append(StringElement('PRODUCT_NAME', '$(TARGET_NAME)'))
        self.project = self.objects.create_project()
        self.project.build_config_list = config_list.reference
        self.project.development_region = 'English'
        self.project.known_regions.append('English')
        self.project.has_scanned_for_encodings = 1;
        #self.project.compatibility_version = 'Xcode 3.2'
        
        self.groups = self.objects.create_group()
        self.project.main_group = self.groups.reference
        self.sources = self.objects.create_group()
        self.sources.name = 'Sources'
        self.products = self.objects.create_group()
        self.products.name = 'Products'
        self.groups.children.append(self.sources.reference)
        self.groups.children.append(self.products.reference)

        self.root_object = self.project.reference
        
    def create_config_list(self, name):
        config = self.objects.create_build_config()
        config.name = name
        config_list = self.objects.create_config_list()
        config_list.default_config_name = config.name
        config_list.build_configs.append(config.reference)
        return config_list, config
               
    def create_native_app_target(self, name):
        file_ref = self.objects.create_file_reference()
        file_ref.explicit_file_type  = 'wrapper.application'
        file_ref.include_in_index = 0
        file_ref.path = '{}.app'.format(name)
        file_ref.source_tree = 'BUILT_PRODUCTS_DIR'
        
        target = self.objects.create_native_target()
        config_list, config = self.create_config_list('Default')
        target.build_config_list = config_list.reference
        target.config = config 
        target.name = name
        target.product_name = name
        target.product_type = 'com.apple.product-type.application'
        target.product_reference = file_ref.reference
                
        self.target = target
        self.project.targets.append(target.reference)
        self.products.children.append(file_ref.reference)
        return target

    def create_native_lib_target(self, name):
        file_ref = self.objects.create_file_reference()
        file_ref.explicit_file_type  = 'archive.ar'
        file_ref.include_in_index = 0
        file_ref.path = 'lib{}.a'.format(name)
        file_ref.source_tree = 'BUILT_PRODUCTS_DIR'

        target = self.objects.create_native_target()
        config_list, config = self.create_config_list('Default')
        target.build_config_list = config_list.reference
        target.config = config 
        target.name = name
        target.product_name = name
        target.product_type = 'com.apple.product-type.library.static'
        target.product_reference = file_ref.reference

        self.target = target
        self.project.targets.append(target.reference)
        self.products.children.append(file_ref.reference)
        return target

    def create_source_buildphase(self):
        bp = self.objects.create_sources_buildphase()
        self.target.build_phases.append(bp.reference)
        return bp

    def create_frameworks_buildphase(self):
        bp = self.objects.create_frameworksbuildphase()
        self.target.build_phases.append(bp.reference)
        return bp

    def add_source_group(self, group, file_refs):
        if not isinstance(group, model.Project):
            grp = self.objects.create_group()
            if group.name:
                grp.name = group.name
            grp.children.extend([f.reference for f in file_refs])
            self.sources.children.append(grp.reference)
            return grp        
        else:
            self.sources.children.extend([f.reference for f in file_refs])
            return self.sources

    def create_build_file(self, file_ref=None):
        bf = self.objects.create_build_file()
        bf.file_ref = file_ref
        return bf

    def create_file_reference(self, type, path):
        fr = self.objects.create_file_reference()
        fr.file_encoding = 4
        fr.last_known_file_type = type
        fr.path = path
        fr.source_tree = '"<absolute>"'
        return fr

    def write(self, filename):
        with open(filename, 'w') as f:
            f.write(self.serialize())
            
    def transform(self):
        rc, _ = utils.execute('xcodebuild -project {}.xcodeproj'.format(self.name))
        if rc != 0:
            raise RuntimeError()


class CXXToolchain(Toolchain):
    def __init__(self, name):
        super(CXXToolchain, self).__init__(name)

    def generate(self, project, toolchain=None):
        toolchain = toolchain if toolchain else self
        cxx_project = CXXProject(toolchain, project.name)

        def add_target(project):
            def key_value(key, value):
                return key if value is None else "{}={}".format(key, value)
            macros = [key_value(macro.key, macro.value) for macro in project.macros if macro.matches(toolchain.name)]
            incpaths = [incpath.path for incpath in project.incpaths if incpath.matches(toolchain.name)]
            libpaths = [libpath.path for libpath in project.libpaths if libpath.matches(toolchain.name)]
        
            if isinstance(project, model.CXXLibrary):
                target = cxx_project.create_native_lib_target(project.name)
            if isinstance(project, model.CXXExecutable):
                target = cxx_project.create_native_app_target(project.name)
                macros += [key_value(macro.key, macro.value) for dep in project.dependencies for macro in dep.macros if macro.publish]
                incpaths += [incpath.path for dep in project.dependencies for incpath in dep.incpaths if incpath.publish]
                libpaths += [libpath.path for dep in project.dependencies for libpath in dep.libpaths if libpath.publish]
                libraries = [dep.name for dep in project.dependencies if isinstance(dep, model.CXXLibrary)]
                libraries  = ['{output}/{lib}/lib{lib}.a'.format(output=toolchain.attributes.output, lib=lib) for lib in libraries]
                for library in libraries:
                    fr = cxx_project.create_file_reference(cxx_project.FILE_TYPE_ARCHIVE, library)
                    bf = cxx_project.create_build_file(fr.reference)
                    cxx_project.create_frameworks_buildphase().files.append(bf.reference)
                    libpaths += [os.path.dirname(library)]
            
            if macros:
                macro_list = ListElement('GCC_PREPROCESSOR_DEFINITIONS')
                macro_list.extend(macros)
                target.config.build_settings.append(macro_list)
            if incpaths:
                incpath_list = ListElement('HEADER_SEARCH_PATHS', quote=True)
                incpath_list.extend(incpaths)
                target.config.build_settings.append(incpath_list)
            if libpaths:
                libpath_list = ListElement('LIBRARY_SEARCH_PATHS', quote=True)
                libpath_list.extend(libpaths)
                target.config.build_settings.append(libpath_list)
            target.config.build_settings.append(StringElement('SDKROOT', 'macosx'))
            target.config.build_settings.append(StringElement('SYMROOT', cxx_project.output))
            target.config.build_settings.append(StringElement('CONFIGURATION_BUILD_DIR', '$(BUILD_DIR)/$(EFFECTIVE_PLATFORM_NAME)'))        

            for dep in project.dependencies:
                add_target(dep)
       
        add_target(project)
        toolchain.apply_features(project, cxx_project)

        sources_by_tool = {}
        groups = project.source_groups + [project]
        for group in groups:
            tool_sources = {}
            for source in group.sources:
                if source.tool not in tool_sources:
                    tool_sources[source.tool] = []
                tool_sources[source.tool].append(source)
            for tool_name in tool_sources:
                tool = toolchain.get_tool(tool_name)
                if tool is None:
                    raise RuntimeError()
                file_refs = tool.transform(cxx_project, tool_sources[tool_name])
                cxx_project.add_source_group(group, file_refs)

        dir = '{project}.xcodeproj'.format(project=project.name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        cxx_project.write('{project}.xcodeproj/project.pbxproj'.format(project=project.name))
        
        return cxx_project

    def transform(self, project):
        cxx_project = self.generate(project)
        cxx_project.transform()
