class Query:
    """Object to encapsulate data of the current query"""

    text = ""
    """statement of the query"""
    communicator = None
    """communicator used to submit query"""
    language = ""
    """language of the query"""

    def __init__(self, text, communicator, language):
        self.text = text
        self.communicator = communicator
        self.language = language

    def get_text(self):
        """@return string text of the query"""
        return self.text

    def set_text(self, text):
        """Setter method
        @param String text"""
        self.text = text

    def get_communicator(self):
        """@return communicator used to submit query"""
        return self.communicator

    def get_language(self):
        """@return string language of the query"""
        return self.language
