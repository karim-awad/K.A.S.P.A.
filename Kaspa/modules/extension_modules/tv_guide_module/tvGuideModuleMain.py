from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.extension_modules.tv_guide_module.tvGuideModuleDe import TvGuideModuleDe


class TvGuideModuleMain(AbstractModule):
    module_name = "TV Guide"

    def __init__(self):
        super(TvGuideModuleMain, self).__init__()
        # doesn't really make sense to translate the german tv guide into english
        self.add_submodule(TvGuideModuleDe())

