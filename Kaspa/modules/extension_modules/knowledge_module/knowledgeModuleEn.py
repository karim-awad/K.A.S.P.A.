from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule
import Kaspa.modules.extension_modules.helper.comandOps as Co
from Kaspa.modules.exceptions.impossibleActionError import ImpossibleActionError


class KnowledgeModuleEn(AbstractSubmodule):
    module_name = "Wolfram Alpha"

    language = "en"

    key_regexes = dict()

    @staticmethod
    def convert_query(query):
        key_strings = [
            "who is ",
            "who was ",
            "what is an ",
            "what is a ",
            "what is the ",
            "what is ",
            "what's an",
            "what's a",
            "what's the",
            "what's",
            "who are ",
            "who were ",
            "what are the ",
            "what are "]

        return Co.get_text_after(query, key_strings)

    def __init__(self):
        self.key_regexes = {'.*': self.action}
        """last module standing"""

    def action(self, query):
        query_text = query.get_text()
        communicator = query.get_communicator()
        try:
            communicator.say(self.main_module.get_wolfram_alpha_answer(query_text))
        except ImpossibleActionError as e:
            # try Wikipedia
            query_text = self.convert_query(query.get_text())
            if query_text is None:
                raise ImpossibleActionError("I can't help you")
            if query_text:
                query_text = str(query_text.title())
                communicator.say(self.main_module.get_wikipedia_description(query_text, self.language))
            else:
                raise ImpossibleActionError("I can't help you")
