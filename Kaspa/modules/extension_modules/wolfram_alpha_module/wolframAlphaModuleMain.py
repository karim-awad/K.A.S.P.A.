import urllib.request
#from PIL import Image
from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.extension_modules.wolfram_alpha_module.wolframAlphaModuleDe import WolframAlphaModuleDe
from Kaspa.modules.extension_modules.wolfram_alpha_module.wolframAlphaModuleEn import WolframAlphaModuleEn
from Kaspa.config import Config
from Kaspa.modules.exceptions.impossibleActionError import ImpossibleActionError


class WolframAlphaModuleMain(AbstractModule):

    module_name = "Wolfram Alpha"

    config_parameters = {"api_key" : "This is the Wolfram Alpha Api Key. You can get it for free from here: \n"
                                     "http://products.wolframalpha.com/api/"}

    api_key = None

    def __init__(self):
        super(WolframAlphaModuleMain, self).__init__()
        self.add_submodule(WolframAlphaModuleDe())
        self.add_submodule(WolframAlphaModuleEn())

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
            # TODO localize
            raise ImpossibleActionError("nope.")
        return response

    def get_picture(self, query):
        query = self.convert_query(query)
        url = "https://api.wolframalpha.com/v1/simple?i=" + query + "%3F&appid=" + self.api_key

        img = urllib.request.urlopen(url).read()
        f = open('/tmp/output', 'wb')
        f.write(img)
        f.close()
        return '/tmp/output'
