from pws import Bing
from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.extension_modules.pc_control_module.pcControlModuleDe import PcControlModuleDe
from Kaspa.modules.extension_modules.pc_control_module.pcControlModuleEn import PcControlModuleEn


class PcControlModuleMain(AbstractModule):

    module_name = "Pc remote"

    def __init__(self):
        super(PcControlModuleMain, self).__init__()
        self.add_submodule(PcControlModuleDe())
        self.add_submodule(PcControlModuleEn())

    def get_link(self, show):
        show = show + " netflix.com/de/title"
        link = Bing.search(show, 5, 0)["results"][0]["link"]
        parts = link.split("title")
        link = parts[0] + "watch" + parts[1]
        return link

