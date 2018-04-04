from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule


class WolframAlphaModuleEn(AbstractSubModule):
    module_name = "Wolfram Alpha"

    language = "en"

    def action(self, query):
        query_text = query.get_text()
        communicator = query.get_communicator()
        communicator.say(self.main_module.get_answer(query_text))

    key_regexes = {'.*': action}
    """last module standing"""
