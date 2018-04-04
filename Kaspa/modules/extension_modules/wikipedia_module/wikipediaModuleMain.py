import wikipedia as wiki
from wikipedia.exceptions import DisambiguationError
from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.exceptions.moduleError import ModuleError
from Kaspa.modules.extension_modules.wikipedia_module.wikipediaModuleDe import WikipediaModuleDe
from Kaspa.modules.extension_modules.wikipedia_module.wikipediaModuleEn import WikipediaModuleEn
import Kaspa.modules.extension_modules.helper.comandOps as Co


class WikipediaModuleMain(AbstractModule):

    module_name = "Wikipedia"

    def __init__(self):
        super(WikipediaModuleMain, self).__init__()
        self.add_submodule(WikipediaModuleDe())
        self.add_submodule(WikipediaModuleEn())

    def get_description(self, query_text, language):
        try:
            wiki.set_lang(language)
            # query_text = wiki.search(query_text)[0]  # search for query and take title of first result
            ret = wiki.summary(query_text)
            return Co.get_sentences(ret, 1) # better than the built in function of the wikipedia module
        except DisambiguationError as disambigError:
            query_text = disambigError.options[0]  # take first guess of meaning
            ret = wiki.summary(query_text)
            return Co.get_sentences(ret, 1)
        except Exception as e:
            raise ModuleError(self.module_name, str(e))
