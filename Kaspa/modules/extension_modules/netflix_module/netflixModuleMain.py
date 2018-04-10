from pws import Bing
from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.extension_modules.netflix_module.netflixModuleDe import NetflixModuleDe
from Kaspa.modules.extension_modules.netflix_module.netflixModuleEn import NetflixModuleEn


class NetflixModuleMain(AbstractModule):

    module_name = "Netflix"

    def __init__(self):
        super(NetflixModuleMain, self).__init__()
        self.add_submodule(NetflixModuleDe())
        self.add_submodule(NetflixModuleEn())

    def get_link(self, show):
        show = show + " netflix.com/de/title"
        link = Bing.search(show, 5, 0)["results"][0]["link"]
        parts = link.split("title")
        link = parts[0] + "watch" + parts[1]
        return link

