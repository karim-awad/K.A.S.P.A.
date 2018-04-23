from Kaspa.communicators.abstract_communicators.abstractTextCommunicator import AbstractTextCommunicator


class NullCommunicator(AbstractTextCommunicator):
    """null communicator to allow using modules without output"""

    def say(self, text):
        self.logger.info(text)
        pass

    def ask(self, question):
        pass

    def run(self):
        pass
