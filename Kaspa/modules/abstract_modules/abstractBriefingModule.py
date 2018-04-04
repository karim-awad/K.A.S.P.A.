from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.moduleManager import ModuleManager as mManager


class AbstractBriefingModule(AbstractModule):
    """Abstract class for briefing modules"""

    # TODO adapt to new language model

    def briefing_action(self, query):
        """this method gets called as part of the briefing functionality of K.A.S.P.A.
            this could e.g be the weather report or the latest news. if the module does not define this method,
            the regular action method gets called
            @param query mainly needed here to retrieve the communicator"""
        self.action(query)

    def activate(self):
        """activates the module"""
        mManager.get_instance().add_module(self)
        mManager.get_instance().add_briefing_module(self)
        self.logger.info(self.__class__.__name__ + " activated")

    def deactivate(self):
        """deactivates the module"""
        mManager.get_instance().remove_module(self)
        mManager.get_instance().remove_briefing_module(self)
        self.logger.info(self.__class__.__name__ + " deactivated")
