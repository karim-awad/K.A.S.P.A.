from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule
from Kaspa.assistantCore import AssistantCore
from Kaspa.communicators.nullCommunicator import NullCommunicator
import json
import re


class MacroModuleEn(AbstractSubmodule):

    module_name = "Macros"

    language = "en"

    macros = dict()

    key_regexes = dict()

    MACRO_PATH = "Kaspa/modules/core_modules/resources/macro_module/" + language + "/macros.json"

    def __init__(self):
        macro_file = open(self.MACRO_PATH)
        self.macros = json.load(macro_file)
        # update regexes
        for key, (answer, commands) in self.macros.items():
            self.key_regexes[key] = self.action
            macro_file.close()

    def action(self, query):
        message = query.get_text()
        communicator = query.get_communicator()
        core = AssistantCore()
        null_communicator = NullCommunicator()

        for key, (answer, commands) in self.macros.items():
            if re.match(key, message):
                communicator.say(answer)
                for command in commands:
                    core.answer(null_communicator, command)
