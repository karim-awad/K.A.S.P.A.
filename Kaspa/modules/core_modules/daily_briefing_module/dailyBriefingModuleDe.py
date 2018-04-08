from Kaspa.modules.abstract_modules.abstractBriefingSubmodule import AbstractBriefingSubmodule
from Kaspa.modules.moduleManager import ModuleManager


class DailyBriefingModuleDe(AbstractBriefingSubmodule):
    module_name = "Briefing"

    language = "de"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=guten morgen)+.': self.action_morning,
                            '(?i).*?(?=zusammenfassung)+.': self.action_regular}

    def briefing(self, query):
        self.main_module.briefing(query)

    def action_morning(self, query):
        communicator = query.get_communicator()
        communicator.say("Guten Morgen! Ich hoffe du hast gut geschlafen. Nun folgt deine tägliche Zusammenfassung")
        self.briefing(query)
        communicator.say("Das wars. Ich wünsche dir einen erfolgreichen Tag!")
        return

    def action_regular(self, query):
        communicator = query.get_communicator()
        communicator.say("Das ist deine heutige Zusammenfassung:")
        self.briefing(query)
        communicator.say("Das wars. Bleib informiert!")
        return
