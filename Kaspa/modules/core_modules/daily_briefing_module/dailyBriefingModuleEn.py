from Kaspa.modules.abstract_modules.abstractBriefingSubmodule import AbstractBriefingSubmodule
from Kaspa.modules.moduleManager import ModuleManager


class DailyBriefingModuleEn(AbstractBriefingSubmodule):
    module_name = "Briefing"

    language = "en"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=Good Morning)+.': self.action_morning,
                            '(?i).*?(?=briefing)+.': self.action_regular}

    def briefing(self, query):
        self.main_module.briefing(query)

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
