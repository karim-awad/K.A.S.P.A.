class ImpossibleActionError(Exception):
    """Used when an action cannot be performed, because it is not possible to achieve.
        These errors messages should be read directly to the user"""
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(ImpossibleActionError, self).__init__(message)
