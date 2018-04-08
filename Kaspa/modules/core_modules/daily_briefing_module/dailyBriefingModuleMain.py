from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.moduleManager import ModuleManager
from Kaspa.modules.core_modules.daily_briefing_module.dailyBriefingModuleDe import DailyBriefingModuleDe
from Kaspa.modules.core_modules.daily_briefing_module.dailyBriefingModuleEn import DailyBriefingModuleEn


class DailyBriefingModuleMain(AbstractModule):

    module_name = "Daily Briefing"

    def __init__(self):
        super(DailyBriefingModuleMain, self).__init__()
        self.add_submodule(DailyBriefingModuleDe())
        self.add_submodule(DailyBriefingModuleEn())

    @staticmethod
    def briefing(query):
        module_manager = ModuleManager.get_instance()
        query.set_text('')
        for briefing_module in module_manager.get_briefing_modules():
            briefing_module.get_submodule(query.get_language()).briefing_action(query)
