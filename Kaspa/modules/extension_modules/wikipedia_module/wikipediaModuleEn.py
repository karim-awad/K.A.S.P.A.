from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule
import Kaspa.modules.extension_modules.helper.comandOps as Co


class WikipediaModuleEn(AbstractSubModule):
    module_name = "Wikipedia"

    language = "en"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i)who+.*': self.action,
                            '(?i)what+.*': self.action}

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

    def action(self, query):
        communicator = query.get_communicator()
        query_text = str(self.convert_query(query.get_text())).title()
        communicator.say(self.main_module.get_description(query_text, self.language))
