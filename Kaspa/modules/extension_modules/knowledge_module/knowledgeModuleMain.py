import urllib.request
import json
#from PIL import Image
from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.extension_modules.knowledge_module.knowledgeModuleDe import KnowledgeModuleDe
from Kaspa.modules.extension_modules.knowledge_module.knowledgeModuleEn import KnowledgeModuleEn
from Kaspa.config import Config
from Kaspa.modules.exceptions.impossibleActionError import ImpossibleActionError
from Kaspa.modules.exceptions.moduleError import ModuleError
import Kaspa.modules.extension_modules.helper.comandOps as Co


import wikipedia as wiki
from wikipedia.exceptions import DisambiguationError


class KnowledgeModuleMain(AbstractModule):

    module_name = "Wolfram Alpha"

    config_parameters = {"api_key" : "This is the Wolfram Alpha Api Key. You can get it for free from here: \n"
                                     "http://products.wolframalpha.com/api/"}

    api_key = None

    url = "http://api.wolframalpha.com/v1/conversation.jsp"
    conversationID = None
    s = None

    def __init__(self):
        super(KnowledgeModuleMain, self).__init__()
        self.add_submodule(KnowledgeModuleDe())
        self.add_submodule(KnowledgeModuleEn())

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

    def get_wolfram_alpha_answer(self, query):
        query = self.convert_query(query)
        if self.conversationID is None:
            url = self.url + "?appid=" + self.api_key + "&i=" + query
        else:
            url = self.url + "?appid=" + self.api_key + "&conversationid=" + self.conversationID + "&i=" + query
            if self.s is not None:
                url = url + "&s=" + self.s
        response = urllib.request.urlopen(url).read().decode('utf-8')
        result = json.loads(response)
        if "error" in result.keys():
            # reset values
            self.url = "http://api.wolframalpha.com/v1/conversation.jsp"
            self.conversationID = None
            self.s = None
            raise ImpossibleActionError("even Wolfram Alpha cannot help")
        self.url = "http://" + result["host"] + "/api/v1/conversation.jsp"
        self.conversationID = result["conversationID"]
        if "s" in result.keys():
            self.s = result["s"]
        else:
            self.s = None
        return Co.get_sentences(result["result"], 1)

    def get_picture(self, query):
        query = self.convert_query(query)
        url = "https://api.wolframalpha.com/v1/simple?i=" + query + "%3F&appid=" + self.api_key

        img = urllib.request.urlopen(url).read()
        f = open('/tmp/output', 'wb')
        f.write(img)
        f.close()
        return '/tmp/output'

    def get_wikipedia_description(self, query_text, language):
        try:
            wiki.set_lang(language)
            # query_text = wiki.search(query_text)[0]  # search for query and take title of first result
            ret = wiki.summary(query_text)
            # TODO improve sentence detection
            return Co.get_sentences(ret, 1) # better than the built in function of the wikipedia module
        except DisambiguationError as disambigError:
            query_text = disambigError.options[0]  # take first guess of meaning
            ret = wiki.summary(query_text)
            return Co.get_sentences(ret, 1)
        except Exception as e:
            raise ModuleError(self.module_name, str(e))
