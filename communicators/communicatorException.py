class CommunicatorException(Exception):

    def __init__(self, module_name, message):

        # Call the base class constructor with the parameters it needs
        super(CommunicatorException, self).__init__(message)
