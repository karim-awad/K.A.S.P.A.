from Kaspa.communicators.abstract_communicators.abstractCommunicator import AbstractCommunicator


class AbstractTextCommunicator(AbstractCommunicator):
    """Abstract class used for text based communication with the user"""

    text_based = True
    """attribute that defines whether the communication module
        uses voice or text based communication"""
