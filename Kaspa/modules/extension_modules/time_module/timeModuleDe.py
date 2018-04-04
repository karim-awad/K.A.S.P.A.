from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule


class TimeModuleDe(AbstractSubModule):

    module_name = "Time"

    language = "de"

    def action(self, query):
        communicator = query.get_communicator()
        communicator.say("Es ist " + self.main_module.time())

    key_regexes = {'(?i).*?(?=wieviel)+.+?(?=uhr)+.': action}
