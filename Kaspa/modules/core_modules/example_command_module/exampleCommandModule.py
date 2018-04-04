from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
import json
import random


class ExampleCommandModule(AbstractModule):
    """the keywords get dynamically loaded from multiple json files"""

    module_name = "Example Commands"

    EXAMPLE_COMMAND_PATH = "Kaspa/modules/exampleCommands.json"

    example_commands = list()

    def __init__(self):
        # iterate over all json files in the directory
        json_file = open(self.EXAMPLE_COMMAND_PATH, "r")
        examples = json.load(json_file)
        for key, answer in examples.items():
            self.example_commands.append(answer)

    def action(self, query):
        communicator = query.get_communicator()
        communicator.say(
            "I can do a lot of things! Just try me. Use commands like: \n" + random.choice(self.example_commands))

    key_regexes = {'(?i).*?(?=what can you do)+.': action}
