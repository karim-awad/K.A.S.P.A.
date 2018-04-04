from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.extension_modules.time_module.timeModuleDe import TimeModuleDe
from Kaspa.modules.extension_modules.time_module.timeModuleEn import TimeModuleEn

import time


class TimeModuleMain(AbstractModule):

    module_name = "Time"

    def __init__(self):
        super(TimeModuleMain, self).__init__()
        self.add_submodule(TimeModuleDe())
        self.add_submodule(TimeModuleEn())

    def time(self):
        return time.strftime("%H:%M")
