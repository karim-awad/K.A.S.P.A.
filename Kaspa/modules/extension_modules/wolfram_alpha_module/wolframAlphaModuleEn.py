from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule


class WolframAlphaModuleEn(AbstractSubModule):
    module_name = "Wolfram Alpha"

    language = "en"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'.*': self.action}
        """last module standing"""

    def action(self, query):
        query_text = query.get_text()
        communicator = query.get_communicator()
        communicator.say(self.main_module.get_answer(query_text))
