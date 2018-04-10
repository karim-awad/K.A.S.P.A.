from Kaspa.modules.abstract_modules.abstractBriefingSubmodule import AbstractBriefingSubmodule
from Kaspa.modules.extension_modules.helper.pcControl import PcControl


class PcControlModuleEn(AbstractBriefingSubmodule):
    module_name = "PC remote"

    language = "en"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=computer|pc)+.+?(?=on)+.': self.action_on,
                            '(?i).*?(?=computer|pc)+.+?(?=off)+.': self.action_off}

    def action_on(self, query):
        communicator = query.get_communicator()
        controller = PcControl()
        if controller.ping():
            communicator.say("Your Computer is already on.")
        else:
            communicator.say("Okay, I'll turn on your computer.")
            controller.on()

    def action_off(self, query):
        communicator = query.get_communicator()
        controller = PcControl()
        if controller.ping():
            controller.off()
            communicator.say("Okay, I'll turn off your computer")
        else:
            communicator.say("Your Computer is already off")

