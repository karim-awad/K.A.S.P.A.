from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule
from textblob import TextBlob


class WolframAlphaModuleDe(AbstractSubmodule):
    module_name = "Wolfram Alpha"

    language = "de"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'.*': self.action}
        """last module standing"""

    def action(self, query):
        query_text = query.get_text()
        query_text = str(TextBlob(query_text).translate(from_lang="de", to="en"))
        communicator = query.get_communicator()
        if "gro" in query.get_text() and "big" in query_text:
            """quick fix because translate always translates gross to big instead of tall and I somehow often ask how
            tall people are"""
            query_text.replace("big", "tall")
        answer = self.main_module.get_answer(query_text)
        answer = str(TextBlob(answer).translate(from_lang="en", to="de"))

        communicator.say(answer)
