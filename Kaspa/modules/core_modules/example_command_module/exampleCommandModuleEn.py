from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule
import random


class ExampleCommandModuleEn(AbstractSubmodule):

    module_name = "Example Commands"

    language = "en"

    EXAMPLE_COMMAND_PATH = \
        "Kaspa/modules/core_modules/resources/example_command_module/" + language + "/exampleCommands.txt"

    example_commands = list()

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=what can you do)+.': self.action}
        file = open(self.EXAMPLE_COMMAND_PATH, "r")
        for line in file.readlines():
            if line.startswith("#"):
                continue
            else:
                self.example_commands.append(line.lstrip("\n"))

    def action(self, query):
        communicator = query.get_communicator()
        communicator.say(
            "I can do a lot of things! Just try me. Use commands like: \n" + random.choice(self.example_commands))