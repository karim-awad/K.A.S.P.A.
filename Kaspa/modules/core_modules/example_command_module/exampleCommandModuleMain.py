from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.core_modules.example_command_module.exampleCommandModuleEn import ExampleCommandModuleEn
from Kaspa.modules.core_modules.example_command_module.exampleCommandModuleDe import ExampleCommandModuleDe


class ExampleCommandModuleMain(AbstractModule):
    """the keywords get dynamically loaded from multiple json files"""

    module_name = "Example Commands"

    def __init__(self):
        super(ExampleCommandModuleMain, self).__init__()

        self.add_submodule(ExampleCommandModuleEn())
        self.add_submodule(ExampleCommandModuleDe())

