from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule


class NewsModuleEn(AbstractSubModule):
    module_name = "News"

    language = "en"

    def action(self, query):
        communicator = query.get_communicator()
        communicator.say(
            "These are the New York Times headlines: \n" + self.main_module.read_rss(
                "http://rss.nytimes.com/services/xml/rss/nyt/World.xml"))

    key_regexes = {'(?i).*?(?=news)+.': action}
