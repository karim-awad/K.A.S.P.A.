from Kaspa.modules.abstract_modules.abstractBriefingSubmodule import AbstractBriefingSubmodule


class TimeModuleDe(AbstractBriefingSubmodule):

    module_name = "Time"

    language = "de"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=wieviel)+.+?(?=uhr)+.': self.action}

    def action(self, query):
        communicator = query.get_communicator()
        communicator.say("Es ist " + self.main_module.time())

    def briefing_action(self, query):
        self.action(query)