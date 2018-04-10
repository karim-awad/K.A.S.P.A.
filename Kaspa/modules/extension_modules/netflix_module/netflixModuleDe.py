from Kaspa.modules.abstract_modules.abstractBriefingSubmodule import AbstractBriefingSubmodule
import Kaspa.modules.extension_modules.helper.comandOps as Co
from Kaspa.modules.extension_modules.helper.pcControl import PcControl


class NetflixModuleDe(AbstractBriefingSubmodule):
    module_name = "Netflix"

    language = "de"

    key_regexes = dict()

    SCRIPT_PATH = '/home/karim/bin/netflixchoose '
    """script that opens chrome with the given link in kiosk mode located on my main pc"""

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=spiele)+.+?(?=auf netflix)+.': self.action_play_show}

    def action_play_show(self, query):
        text = query.get_text()
        communicator = query.get_communicator()
        name = Co.get_text_after(text, ["spiele"])
        name = Co.filter_string(name, "auf netflix")
        link = self.main_module.get_link(name)
        PcControl().run_remote_command(self.SCRIPT_PATH + link + ' &')
        communicator.say("Okay, ich spiele jetzt " + name + " auf Netflix.")




