from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule
from textblob import TextBlob


class WolframAlphaModuleDe(AbstractSubModule):
    module_name = "Wolfram Alpha"

    language = "de"

    def action(self, query):
        query_text = query.get_text()
        query_text = str(TextBlob(query_text).translate(from_lang="de", to="en"))
        communicator = query.get_communicator()
        answer = self.main_module.get_answer(query_text)
        answer = str(TextBlob(answer).translate(from_lang="en", to="de"))

        communicator.say(answer)

    key_regexes = {'.*': action}
    """last module standing"""
