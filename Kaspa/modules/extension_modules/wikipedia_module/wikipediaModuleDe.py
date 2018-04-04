from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule
import Kaspa.modules.extension_modules.helper.comandOps as Co


class WikipediaModuleDe(AbstractSubModule):
    module_name = "Wikipedia"

    language = "de"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i)wer+.*': self.action,
                            '(?i)was+.*': self.action}

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

    def action(self, query):
        communicator = query.get_communicator()
        query_text = str(self.convert_query(query.get_text())).title()
        communicator.say(self.main_module.get_description(query_text, self.language))
