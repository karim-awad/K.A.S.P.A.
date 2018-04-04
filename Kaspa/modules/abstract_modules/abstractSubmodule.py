import logging
from Kaspa.modules.moduleManager import ModuleManager as mManager
from Kaspa.modules.submoduleManager import SubmoduleManager
import Kaspa.strings.strings as strings


class AbstractSubModule(object):
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

    main_module = None

    def configure(self):
        """reads its needed parameters from the config file"""
        self.logger.info(self.__class__.__name__ + " is configured")
        # self.strings = strings.get_strings(self.__class__.__name__)

    def get_config_parameters(self):
        """Getter Method
            @return dictm config parameters and their respective description"""
        return self.config_parameters

    def get_name(self):
        """Getter Method
            @return String name"""
        return self.module_name

    def set_main_module(self, main_module):
        self.main_module = main_module

    def get_language(self):
        return self.language

    def get_key_regexes(self):
        """Getter Method
            @return dict of key_regexes"""
        return self.key_regexes
