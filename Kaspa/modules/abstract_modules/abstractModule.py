import logging
from Kaspa.modules.moduleManager import ModuleManager as mManager


class AbstractModule(object):
    """Abstract class for all plugin modules"""

    logger = logging.getLogger('Kaspa')

    key_regexes = dict()
    """if command matches this, action gets triggered"""

    module_name = ""
    """name of the module"""

    strings = dict()

    config_parameters = dict()
    """A dictionary, that consists of the parameters and their respective description"""

    language = ''

    submodules = dict()

    def __init__(self):
        self.submodules = dict()

    def get_submodule(self, language):
        if language in self.submodules:
            return self.submodules[language]
        else:
            return None

    def add_submodule(self, submodule):
        self.submodules.update({submodule.get_language(): submodule})
        submodule.set_main_module(self)

    def configure(self):
        """reads its needed parameters from the config file"""
        self.logger.info(self.__class__.__name__ + " is configured")
        # self.strings = strings.get_strings(self.__class__.__name__)

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

    def get_language(self):
        return self.language

    def get_key_regexes(self):
        """Getter Method
            @return dict of key_regexes"""
        return self.key_regexes
