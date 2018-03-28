from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.moduleManager import ModuleManager as mManager


class AbstractMediaModule(AbstractModule):
    """Abstract class for media modules, this allows e.g communicators to pause all media while listening"""

    def play(self):
        """play media"""
        raise NotImplementedError("Missing implementation")
        pass

    def pause(self):
        """pause media"""
        raise NotImplementedError("Missing implementation")
        pass

    def is_playing(self):
        """get state of player
        @return bool true if currently playing"""
        raise NotImplementedError("Missing implementation")
        pass

    def activate(self):
        """activates the module"""
        mManager.get_instance().add_module(self)
        mManager.get_instance().add_media_module(self)
        self.logger.info(self.__class__.__name__ + " activated")

    def deactivate(self):
        """deactivates the module"""
        mManager.get_instance().remove_module(self)
        mManager.get_instance().remove_media_module(self)
        self.logger.info(self.__class__.__name__ + " deactivated")
