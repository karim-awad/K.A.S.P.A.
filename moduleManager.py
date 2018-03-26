class ModuleManager(object):
    """Object to manage all modules"""

    instance = None

    class __ModuleManager:

        modules = list()
        """List of all manageable modules"""

        def add_module(self, module):
            """adds module to the list
                @param module module to be added"""
            self.modules.append(module)

        def remove_module(self, module):
            """removes module from the list
                @param module module to be removed"""
            self.modules.remove(module)

        def get_modules(self):
            """@return list of all modules"""
            return self.modules

    @staticmethod
    def get_instance():
        """implementation of singleton design pattern"""
        if ModuleManager.instance is None:
            ModuleManager.instance = ModuleManager.__ModuleManager()
        return ModuleManager.instance
