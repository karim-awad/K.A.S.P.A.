from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule
from textblob import TextBlob
import Kaspa.modules.extension_modules.helper.comandOps as Co
from Kaspa.modules.exceptions.impossibleActionError import ImpossibleActionError


class KnowledgeModuleDe(AbstractSubmodule):
    module_name = "Wolfram Alpha"

    language = "de"

    key_regexes = dict()

    @staticmethod
    def convert_query(query):
        key_strings = [
            "wer ist ",
            "wer war ",
            "was ist ein ",
            "was ist eine ",
            "was ist der ",
            "was ist die ",
            "was ist das ",
            "was ist ",
            "wer sind die",
            "who waren die ",
            "was sind die"]

        return Co.get_text_after(query, key_strings)

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
            query_text = query_text.replace("big", "tall")
        try:
            answer = self.main_module.get_wolfram_alpha_answer(query_text)
            answer = str(TextBlob(answer).translate(from_lang="en", to="de"))
            communicator.say(answer)
        except ImpossibleActionError as e:
            # try Wikipedia
            query_text = self.convert_query(query.get_text())
            if query_text is None:
                raise ImpossibleActionError("da kann ich dir leider nicht weiterhelfen.")
            if query_text:
                query_text = str(query_text.title())
                communicator.say(self.main_module.get_wikipedia_description(query_text, self.language))
            else:
                raise ImpossibleActionError("da kann ich dir leider nicht weiterhelfen.")