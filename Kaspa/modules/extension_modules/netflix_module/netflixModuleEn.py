from Kaspa.modules.abstract_modules.abstractBriefingSubmodule import AbstractBriefingSubmodule
import Kaspa.modules.extension_modules.helper.comandOps as Co
from Kaspa.modules.extension_modules.helper.pcControl import PcControl


class NetflixModuleEn(AbstractBriefingSubmodule):
    module_name = "Netflix"

    language = "en"

    key_regexes = dict()

    SCRIPT_PATH = '/home/karim/bin/netflixchoose '
    """script that opens chrome with the given link in kiosk mode located on my main pc"""

    SCRIPT_PLAY_PAUSE_PATH = '/home/karim/bin/netflixpp '
    """script that pauses/plays netflix on my pc"""

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=play)+.+?(?=on netflix)+.': self.action_play_show,
                            '(?i).*?(?=continue)+.+?(?=netflix)+.': self.action_pause_play,
                            '(?i).*?(?=paus)+.+?(?=netflix)+.': self.action_pause_play}

    def action_play_show(self, query):
        text = query.get_text()
        communicator = query.get_communicator()
        name = Co.get_text_after(text, ["play"])
        name = Co.filter_string(name, "on netflix")
        link = self.main_module.get_link(name)
        PcControl().run_remote_command(self.SCRIPT_PATH + link + ' &')
        communicator.say("Okay, playing " + name + " on Netflix.")

    def action_pause_play(self, query):
        communicator = query.get_communicator()
        PcControl().run_remote_command(self.SCRIPT_PLAY_PAUSE_PATH + ' &')
        communicator.say("Okay!")
