from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule
import urllib.request
from bs4 import BeautifulSoup as bs


class TvGuideModuleDe(AbstractSubmodule):
    module_name = "TV Guide"

    language = "de"

    key_regexes = dict()

    channels = ["kabel eins", "RTL", "Das Erste", "SAT.1", "COMEDY CENTRAL", "ZDF", "VOX", "ProSieben"]

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=abend)+.+?(?=fernseh)+.': self.action_primetime,
                            '(?i).*?(?=fernseh)+.': self.action_now}

    def tell_guide(self, query, url):
        communicator = query.get_communicator()

        response = urllib.request.urlopen(url).read()
        soup = bs(response, features="xml")
        items = soup.findAll("item")
        answer = ' '
        for item in items:
            for channel in self.channels:
                if channel in item.title.string:
                    titleparts = item.title.string.split("|")
                    answer = answer + titleparts[1] + "zeigt ab " + titleparts[0] + titleparts[2] + "\n\n"
        communicator.say(answer)

    def action_now(self, query):
        url = "http://www.tvspielfilm.de/tv-programm/rss/jetzt.xml"
        self.tell_guide(query, url)

    def action_primetime(self, query):
        url = "http://www.tvspielfilm.de/tv-programm/rss/heute2015.xml"
        self.tell_guide(query, url)

