from configparser import ConfigParser
from configparser import RawConfigParser
# from Kaspa.communicators.commandlineCommunicator import CommandlineCommunicator
from Kaspa.modules.moduleManager import ModuleManager
import os


class Config(object):
    instance = None
    CONFIG_NAME = "Kaspa.cfg"

    class __Config:

        config = None
        path = None

        def __init__(self, path="str(Path.home())"):
            """initializes config file
                @param path path where config should be stored"""
            self.path = path
            self.config = ConfigParser()
            self.load()

        def get(self, section, key):
            """retrieves value from config file
                @param section section where the value is located
                @param key key of the value
                @return value"""
            return self.config.get(section, key)

        def get_section_content(self, section):
            """@return dictionary of all keys of the given section"""
            return self.config.items(section)

        # def populate(self):
        #     """creates a personalized config file"""
        #
        #     config = RawConfigParser()
        #     communicator = CommandlineCommunicator()
        #     communicator.say("Hello, I am Kaspa, your new Personal Assistant. I couldn't find a configuration file in "
        #                      "your config directory: " + self.path)
        #
        #     if not communicator.ask_bool("Do you want me to help you create one now?"):
        #         communicator.say("Okay, then I am going to sleep now, as I am pretty much useless without a config "
        #                          "file. Run me again, when you have created one")
        #         exit(0)
        #
        #     module_manager = ModuleManager.get_instance()
        #     for module in module_manager.get_modules():
        #         if not communicator.ask_bool("Do you want to use the " + module.get_name() + " module?"):
        #             # TODO disable possibility to turn of core modules
        #             module.deactivate()
        #             continue
        #
        #         config.add_section(module.get_name())
        #         if not module.get_config_parameters():
        #             continue
        #
        #         for parameter, description in module.get_config_parameters().items():
        #             value = communicator.ask(parameter + "\n" + description + "\n" + "What value do you want to "
        #                                                                              "set it to?")
        #             config.set(module.get_name(), parameter, value)
        #
        #     with open(self.path + Config.CONFIG_NAME, 'w') as configfile:
        #         config.write(configfile)
        #         self.load()
        #
        #     communicator.say("That's it. I am already looking forward to helping you!")
        #     # TODO fix bugs

        def load(self):
            """reloads the config file"""
            self.config.read(self.path + Config.CONFIG_NAME)

        def load_modules(self):
            module_manager = ModuleManager.get_instance()

            for module in module_manager.get_modules():
                module.configure()

    @staticmethod
    def get_instance():
        """implementation of singleton design pattern"""
        if Config.instance is None:
            Config.instance = Config.__Config()
        return Config.instance

    @staticmethod
    def set_instance(path):
        """implementation of singleton design pattern
        @param path String where config should be stored"""
        Config.instance = Config.__Config(path)
        if not os.path.exists(path + Config.CONFIG_NAME):
            Config.instance.populate()
