class ModuleError(Exception):
    """used for unexpected errors"""
    def __init__(self, module_name, message):

        # Call the base class constructor with the parameters it needs
        super(ModuleError, self).__init__(module_name + ": " + message)
