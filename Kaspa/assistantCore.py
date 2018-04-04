import logging
import re
from Kaspa.query import Query
from Kaspa.modules.moduleManager import ModuleManager as mManager
from Kaspa.modules.exceptions.moduleError import ModuleError
from Kaspa.modules.exceptions.impossibleActionError import ImpossibleActionError
import Kaspa.strings.strings as strings
from Kaspa.config import Config


class AssistantCore(object):
    logger = logging.getLogger('Kaspa')
    strings = dict()

    def __init__(self):
        self.strings = strings.get_strings("assistantCore")

    def answer(self, communicator, message):
        """let the assistant answer to the given message
            @param communicator the communicator object used for communication
            @param message string, the assistant should answer to"""
        language = Config.get_instance().get("general", "language")
        query = Query(message.lower(), communicator, language)
        modules = mManager.get_instance().get_modules()
        if not modules:
            communicator.say(self.strings["NO_MODULES"])
            return
        for module in modules:
            """traverse modules and match their regex keys"""
            module = module.get_submodule(query.get_language())
            if module is not None:
                for key_regex, method in module.get_key_regexes().items():
                    if re.match(key_regex, message):
                        try:
                            method(query)
                        except ImpossibleActionError as e:
                            communicator.say(self.strings["KNOWN_ERROR"] + str(e))
                        except ModuleError as e:
                            communicator.say(self.strings["UNKNOWN_ERROR"])
                            self.logger.error(str(e))
                        return
        communicator.say(self.strings["NOT_PROCESSABLE"])

