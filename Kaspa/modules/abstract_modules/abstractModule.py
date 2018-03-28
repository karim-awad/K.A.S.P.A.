import logging
from Kaspa.modules.moduleManager import ModuleManager as mManager


class AbstractModule(object):
    """Abstract class for all plugin modules"""

    logger = logging.getLogger('Kaspa')

    key_regexes = list()
    """if command matches this, action gets triggered"""

    module_name = ""
    """name of the module"""

    config_parameters = dict()
    """A dictionary, that consists of the parameters and their respective description"""

    def action(self, query):
        """the real function of the Module
            @param query object used to store details of query"""
        raise NotImplementedError("Missing implementation")
        pass

    def configure(self):
        """reads its needed parameters from the config file"""
        self.logger.info(self.__class__.__name__ + " is configured")

    def activate(self):
        """activates the module"""
        mManager.get_instance().add_module(self)
        self.logger.info(self.__class__.__name__ + " activated")

    def deactivate(self):
        """deactivates the module"""
        mManager.get_instance().remove_module(self)
        self.logger.info(self.__class__.__name__ + " deactivated")

    def get_config_parameters(self):
        """Getter Method
            @return dictm config parameters and their respective description"""
        return self.config_parameters

    def get_name(self):
        """Getter Method
            @return String name"""
        return self.module_name

    def get_key_regexes(self):
        """Getter Method
            @return list of key_regexes"""
        return self.key_regexes
