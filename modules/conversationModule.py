from abstractModule import AbstractModule
import json
import re
import os


class ConversationModule(AbstractModule):

    key_regexes = list()
    """the keywords get dynamically loaded from multiple json files"""

    module_name = "Conversation"

    conversations = dict()

    def __init__(self):
        # iterate over all json files in the directory
        self.logger.info("loading the conversation files...")
        conversation_dir = os.listdir("modules/resources/conversations")
        for file in conversation_dir:
            if ".json" in file:
                json_file = open("modules/resources/conversations/" + file, "r")
                # merge two dictionaries
                self.conversations = {**json.load(json_file), **self.conversations}
                self.logger.info(file + " loaded")
        # update regexes
        for key, answer in self.conversations.items():
            self.key_regexes.append(key)

    def action(self, query):
        message = query.get_text()
        communicator = query.get_communicator()

        for key, answer in self.conversations.items():
            if re.match(key, message):
                communicator.say(answer)
