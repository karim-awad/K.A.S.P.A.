from Kaspa.communicators.abstract_communicators.abstractTextCommunicator import AbstractTextCommunicator
from Kaspa.assistantCore import AssistantCore


class CommandlineCommunicator(AbstractTextCommunicator):
    """simple communicator for commandline usage"""

    def say(self, text):
        print(self.strings["KASPA_CHAT"] + text)

    def ask(self, question):
        return input(self.strings["KASPA_CHAT"] + question + "\n" + self.strings["USERCHAT"])

    def start_conversation(self):
        core = AssistantCore()
        self.say(self.strings["WELCOME"])
        while True:
            query_text = input(self.strings["USER_CHAT"])
            core.answer(self, query_text)
