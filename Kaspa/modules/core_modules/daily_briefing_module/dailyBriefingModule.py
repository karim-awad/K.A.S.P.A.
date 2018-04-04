from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.moduleManager import ModuleManager


class DailyBriefingModule(AbstractModule):

    module_name = "Daily Briefing"

    @staticmethod
    def briefing(query):
        module_manager = ModuleManager.get_instance()
        query.set_text('')
        for briefing_module in module_manager.get_briefing_modules():
            briefing_module.briefing_action(query)

    def action_morning(self, query):
        communicator = query.get_communicator()
        communicator.say("Good Morning, I hope you slept well. This is your daily briefing.")
        self.briefing(query)
        communicator.say("That's it, have a nice day!")
        return

    def action_regular(self, query):
        communicator = query.get_communicator()
        communicator.say("Hello, what's up? This is your daily briefing.")
        self.briefing(query)
        communicator.say("That's it, stay informed!")
        return

    key_regexes = {'(?i).*?(?=Good Morning)+.': action_morning,
                   '(?i).*?(?=briefing)+.': action_regular}
