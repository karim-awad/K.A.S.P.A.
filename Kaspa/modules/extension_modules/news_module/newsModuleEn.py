from Kaspa.modules.abstract_modules.abstractBriefingSubmodule import AbstractBriefingSubmodule


class NewsModuleEn(AbstractBriefingSubmodule):
    module_name = "News"

    language = "en"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=news)+.': self.action}

    def action(self, query):
        communicator = query.get_communicator()
        communicator.say(
            "These are the New York Times headlines: \n" + self.main_module.read_rss(
                "http://rss.nytimes.com/services/xml/rss/nyt/World.xml"))

    def briefing_action(self, query):
        self.action(query)