from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.moduleManager import ModuleManager


class DailyBriefingModule(AbstractModule):

    key_regexes = ['(?i).*?(?=Good Morning)+.', '(?i).*?(?=briefing)+.']

    module_name = "Daily Briefing"

    @staticmethod
    def briefing(query):
        module_manager = ModuleManager.get_instance()
        query.set_text('')
        for briefing_module in module_manager.get_briefing_modules():
            briefing_module.briefing_action(query)

    def action(self, query):
        communicator = query.get_communicator()
        text = query.get_text()
        if "good morning" in text:
            communicator.say("Good Morning, I hope you slept well. This is your daily briefing.")
            self.briefing(query)
            communicator.say("That's it, have a nice day!")
            return

        if "briefing" in text:
            communicator.say("Hello, what's up? This is your daily briefing.")
            self.briefing(query)
            communicator.say("That's it, stay informed!")
            return
