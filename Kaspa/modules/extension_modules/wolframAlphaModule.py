import urllib.request
#from PIL import Image
from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.config import Config


class WolframAlphaModule(AbstractModule):

    key_regexes = ['.*']
    """last module standing"""

    module_name = "Wolfram Alpha"

    config_parameters = {"api_key" : "This is the Wolfram Alpha Api Key. You can get it for free from here: \n"
                                     "http://products.wolframalpha.com/api/"}

    api_key = None

    def configure(self):
        self.api_key = Config.get_instance().get('wolfram alpha', 'api_key')

    @staticmethod
    def convert_query(orig_query):
        new_query = orig_query.replace(" ", "+")
        return new_query

    def get_answer(self, query):
        query = self.convert_query(query)
        try:
            url = "http://api.wolframalpha.com/v1/result?appid=" + self.api_key + "&i=" + query

            response = urllib.request.urlopen(url).read().decode('utf-8')
        except:
            # TODO Exception handling
            response = "Hmmm"
        return response

    def get_picture(self, query):
        query = self.convert_query(query)
        url = "https://api.wolframalpha.com/v1/simple?i=" + query + "%3F&appid=" + self.api_key

        img = urllib.request.urlopen(url).read()
        f = open('/tmp/output', 'wb')
        f.write(img)
        f.close()
        return '/tmp/output'

    def action(self, query):
        query_text = query.get_text()
        communicator = query.get_communicator()
        communicator.say(self.get_answer(query_text))

