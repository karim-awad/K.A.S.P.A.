from communicators.abstract_communicators.abstractCommunicator import AbstractCommunicator


class AbstractVoiceCommunicator(AbstractCommunicator):
    """Abstract class used for text based communication with the user"""

    text_based = False
    """attribute that defines whether the communication module
        uses voice or text based communication"""
