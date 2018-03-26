from abstractCommunicator import AbstractCommunicator
import assistantCore as Core


class CommandlineCommunicator(AbstractCommunicator):
    """simple communicator for commandline usage"""

    text_based = True

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

