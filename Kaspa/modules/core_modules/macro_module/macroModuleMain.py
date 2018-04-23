from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.core_modules.macro_module.macroModuleEn import MacroModuleEn
from Kaspa.modules.core_modules.macro_module.macroModuleDe import MacroModuleDe


class MacroModuleMain(AbstractModule):

    module_name = "Macros"

    def __init__(self):
        super(MacroModuleMain, self).__init__()

        self.add_submodule(MacroModuleEn())
        self.add_submodule(MacroModuleDe())

