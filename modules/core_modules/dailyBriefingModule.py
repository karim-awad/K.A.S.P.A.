from modules.abstract_modules.abstractModule import AbstractModule
from modules.moduleManager import ModuleManager


class DailyBriefingModule(AbstractModule):
    key_regexes = ['(?i).*?(?=Good Morning)+.']

    module_name = "Daily Briefing"

    def action(self, query):
        communicator = query.get_communicator()
        communicator.say("Good Morning, I hope you slept well. This is your daily briefing.")
        module_manager = ModuleManager.get_instance()
        query.set_text('')
        for briefing_module in module_manager.get_briefing_modules():
            briefing_module.briefing_action(query)
        communicator.say("That's it, have a nice day!")
