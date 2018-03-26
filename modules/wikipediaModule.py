import wikipedia as wiki
import modules.helper.comandOps as Co
from abstractModule import AbstractModule


class WikipediaModule(AbstractModule):

    key_regexes = ['(?i)who+.*', '(?i)what+.*']

    module_name = "Wikipedia"

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

    def get_description(self, query_text):
        try:
            query_text = str(self.convert_query(query_text)).title()
            ret = wiki.summary(query_text)
            return Co.get_sentences(ret, 1)
        except:
            # TODO better exception handling
            return "Sorry, I can't answer that"

    def action(self, query):
        communicator = query.get_communicator()
        query_text = query.get_text()
        communicator.say(self.get_description(query_text))
