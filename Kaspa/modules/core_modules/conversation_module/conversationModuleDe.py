import json
import re
import os
from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule


class ConversationModuleDe(AbstractSubModule):

    keywords = dict()

    module_name = "Conversation"

    conversations = dict()

    language = "de"

    CONVERSATIONS_PATH = "Kaspa/modules/core_modules/conversation_module/resources/" + language + "/conversations/"

    def __init__(self):
        # iterate over all json files in the directory
        self.logger.info("loading the conversation files...")
        conversation_dir = os.listdir(self.CONVERSATIONS_PATH)
        for file in conversation_dir:
            if ".json" in file:
                json_file = open(self.CONVERSATIONS_PATH + file, "r")
                # merge two dictionaries
                self.conversations = {**json.load(json_file), **self.conversations}
                self.logger.info(file + " loaded")
        # update regexes
        for key, answer in self.conversations.items():
            self.key_regexes[key] = self.action

    def action(self, query):
        message = query.get_text()
        communicator = query.get_communicator()

        for key, answer in self.conversations.items():
            if re.match(key, message):
                communicator.say(answer)
