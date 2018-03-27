class ModuleManager(object):
    """Object to manage all modules"""

    instance = None

    class __ModuleManager:

        modules = list()
        """List of all manageable modules"""

        briefing_modules = list()
        """List of all manageable briefing modules"""

        media_modules = list()
        """List of all manageable media modules"""

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

        def add_briefing_module(self, briefing_module):
            """adds module to the list
                @param briefing_module module to be added"""
            self.briefing_modules.append(briefing_module)

        def remove_briefing_module(self, briefing_module):
            """removes briefing module from the list
                @param briefing_module module to be removed"""
            self.briefing_modules.remove(briefing_module)

        def get_briefing_modules(self):
            """@return list of all briefing_modules"""
            return self.media_modules

        def add_media_module(self, media_module):
            """adds module to the list
                @param media_module module to be added"""
            self.media_modules.append(media_module)

        def remove_media_module(self, media_module):
            """removes briefing module from the list
                @param media_module module to be removed"""
            self.media_modules.remove(media_module)

        def get_media_modules(self):
            """@return list of all briefing_modules"""
            return self.media_modules

    @staticmethod
    def get_instance():
        """implementation of singleton design pattern"""
        if ModuleManager.instance is None:
            ModuleManager.instance = ModuleManager.__ModuleManager()
        return ModuleManager.instance
