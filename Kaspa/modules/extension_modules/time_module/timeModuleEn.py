from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule


class TimeModuleEn(AbstractSubmodule):

    module_name = "Time"

    language = "en"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=what)+.+?(?=time)+.': self.action}

    def action(self, query):
        communicator = query.get_communicator()
        communicator.say("It's " + self.main_module.time())