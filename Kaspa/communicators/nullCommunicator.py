from Kaspa.communicators.abstract_communicators.abstractCommunicator import AbstractCommunicator


class NullCommunicator(AbstractCommunicator):
    """null communicator to allow using modules without output"""

    def __init__(self, text_based):
        super().__init__()
        self.text_based = text_based

    def say(self, text):
        pass

    def ask(self, question):
        pass

    def run(self):
        pass
