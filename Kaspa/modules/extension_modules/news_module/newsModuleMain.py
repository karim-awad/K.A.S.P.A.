import urllib.request
from bs4 import BeautifulSoup as Bs
from Kaspa.modules.abstract_modules.abstractBriefingModule import AbstractBriefingModule
from Kaspa.modules.extension_modules.news_module.newsModuleDe import NewsModuleDe
from Kaspa.modules.extension_modules.news_module.newsModuleEn import NewsModuleEn


class NewsModuleMain(AbstractBriefingModule):

    module_name = "News"

    def __init__(self):
        super(NewsModuleMain, self).__init__()
        self.add_submodule(NewsModuleDe())
        self.add_submodule(NewsModuleEn())

    @staticmethod
    def read_rss(url):
        response = urllib.request.urlopen(url).read()
        soup = Bs(response, features="xml")

        items = soup.findAll("item")
        news = ''
        count = 5
        for item in items:
            news = news + item.title.string + "\n" + item.description.string + "\n\n"
            if count is 0:
                break
            else:
                count -= 1
        return news

