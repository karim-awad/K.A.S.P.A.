from communicators.abstract_communicators.abstractTextCommunicator import AbstractTextCommunicator
import assistantCore as Core


class CommandlineCommunicator(AbstractTextCommunicator):
    """simple communicator for commandline usage"""

    def say(self, text):
        print("Kaspa: " + text)

    def ask(self, question):
        return input("Kaspa: " + question + "\nYou: ")

    def start_conversation(self):
        while True:
            query_text = self.ask("How can I help you")
            if input is "quit":
                self.say("Goodbye")
                break
            Core.answer(self, query_text)

