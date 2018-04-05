from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule
import random


class ExampleCommandModuleDe(AbstractSubModule):
    module_name = "Example Commands"

    language = "de"

    EXAMPLE_COMMAND_PATH = \
        "Kaspa/modules/core_modules/resources/example_command_module/" + language + "/exampleCommands.txt"

    example_commands = list()

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=was kannst du)+.': self.action}

        file = open(self.EXAMPLE_COMMAND_PATH, "r")
        for line in file.readlines():
            if line.startswith("#"):
                continue
            else:
                self.example_commands.append(line.strip("\n"))

    def action(self, query):
        communicator = query.get_communicator()
        communicator.say(
            "Ich kann sehr vieles, versuche zum Beispiel mal folgendes: \n" + random.choice(self.example_commands))
