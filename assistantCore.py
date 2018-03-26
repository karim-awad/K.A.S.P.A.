import logging
import re
#from langdetect import detect
from query import Query
from moduleManager import ModuleManager as mManager

logger = logging.getLogger('Kaspa')


def answer(communicator, message):
    """let the assistant answer to the given message
        @param communicator the communicator object used for communication
        @param message string, the assistant should answer to"""

    query = Query(message.lower(), communicator, "en")  # detect(message))
    modules = mManager.get_instance().get_modules()
    if not modules:
        communicator.say("Sorry, there are no modules installed")
        return
    for module in modules:
        """traverse modules and match their regex keys"""
        for key_regex in module.get_key_regexes():
            if re.match(key_regex, message):
               # try:
                module.action(query)
               # except Exception as e:
                    #communicator.say("I am sorry, something went wrong. Check the logs for more information.")
                    #logger.error(str(e))
                return
    communicator.say("Sorry, I don't know how to process that!")

