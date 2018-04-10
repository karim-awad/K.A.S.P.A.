from Kaspa.modules.abstract_modules.abstractBriefingSubmodule import AbstractBriefingSubmodule
import Kaspa.modules.extension_modules.helper.comandOps as Co
from Kaspa.modules.extension_modules.helper.pcControl import PcControl


class PcControlModuleDe(AbstractBriefingSubmodule):
    module_name = "Pc Fernbedienung"

    language = "de"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=computer|pc|rechner)+.+?(?=an|ein)+.': self.action_on,
                            '(?i).*?(?=computer|pc|rechner)+.+?(?=aus)+.': self.action_off}

    def action_on(self, query):
        communicator = query.get_communicator()
        controller = PcControl()
        if controller.ping():
            communicator.say("Dein Computer ist schon eingeschlaten.")
        else:
            communicator.say("Okay, ich schalte deinen Computer ein.")
            controller.on()

    def action_off(self, query):
        communicator = query.get_communicator()
        controller = PcControl()
        if controller.ping():
            controller.off()
            communicator.say("Okay, ich schalte deinen Computer ab.")
        else:
            communicator.say("Dein Computer ist schon aus.")





