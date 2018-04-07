import logging
import Kaspa.strings.strings as strings
from threading import Thread


class AbstractCommunicator(Thread):
    """Abstract class used for communication with the user"""

    logger = logging.getLogger('Kaspa')

    text_based = True
    """attribute that defines whether the communication module
        uses voice or text based communication"""

    strings = dict()

    def __init__(self, class_name=None):
        super().__init__()
        self.logger.info(self.__class__.__name__ + " activated")
        if class_name is None:
            self.strings = strings.get_strings(self.__class__.__name__)
        else:
            self.strings = strings.get_strings(class_name)


    def say(self, text):
        """Method that communicates text to the user
            @param text string to be communicated"""
        raise NotImplementedError("Missing implementation")
        pass

    def ask(self, text):
        """Method to ask a question to the user
            @param text question to be asked
            @return String answer"""
        raise NotImplementedError("Missing implementation")
        pass

    def ask_bool(self, text):
        """Method to ask a yes, no question
            @param text question to be asked
            @return Bool answer"""
        true_answers = ["yes", "true", "yep", "yeah", "ok"]
        false_answers = ["no", "false", "nope"]

        text = self.ask(text)
        for answer in true_answers:
            if answer in text.lower():
                return True
        for answer in false_answers:
            if answer in text.lower():
                return False
        return self.ask_bool("I am sorry, I didn't understand that. Please try answering with a clear Yes or No.")

    def run(self):
        """starts a conversation with the user"""
        raise NotImplementedError("Missing implementation")
        pass

    def is_text_based(self):
        """Getter Method
            @return boolean text_based"""
        return self.text_based
