import logging
import os
from config import Config
from pathlib import Path
from modules.conversationModule import ConversationModule
from modules.googleMapsModule import GoogleMapsModule
from modules.hueModule import HueModule
from modules.newsModule import NewsModule
from modules.redditModule import RedditModule
from modules.mensaModule import MensaModule
from modules.timeModule import TimeModule
from modules.weatherModule import WeatherModule
from modules.wikipediaModule import WikipediaModule
from modules.wolframAlphaModule import WolframAlphaModule

from moduleException import ModuleException

# from voiceCommunicator import VoiceCommunicator
from communicators.commandlineCommunicator import CommandlineCommunicator

logger = None


def init_modules():
    """initializes the wanted modules"""
    try:
        conversation_module = ConversationModule()
        conversation_module.activate()

        google_maps_module = GoogleMapsModule()
        google_maps_module.activate()

        hue_module = HueModule()
        hue_module.activate()

        news_module = NewsModule()
        news_module.activate()

        reddit_module = RedditModule()
        reddit_module.activate()

        mensa_module = MensaModule()
        mensa_module.activate()

        time_module = TimeModule()
        time_module.activate()

        weather_module = WeatherModule()
        weather_module.activate()

        wikipedia_module = WikipediaModule()
        wikipedia_module.activate()

        wolfram_alpha_module = WolframAlphaModule()
        wolfram_alpha_module.activate()

        # TODO activated get modules from config

    except ModuleException as e:
        logger.error(e.message())
        print(e.message())
        exit(1)


def start_communicators():
    """starts all wanted communicators"""
    # vc = VoiceCommunicator()
    clc = CommandlineCommunicator()

    clc.start_conversation()


def main():
    """starts Kaspa with desired modules and communicators"""

    # Initialize config directory
    config_dir_path = str(Path.home()) + "/.config/Kaspa/"
    if not os.path.exists(config_dir_path):
        os.makedirs(config_dir_path)
        print("Created Folder" + config_dir_path)

    # Initialize Logger
    logger = logging.getLogger("Kaspa")
    handler = logging.FileHandler(config_dir_path + '/Kaspa.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # add modules
    logger.info("Loading Modules...")
    init_modules()

    # Initialize Config
    Config.set_instance(config_dir_path)
    Config.get_instance().modules_load()

    # start communicators
    logger.info("Starting Communicators...")
    start_communicators()


if __name__ == "__main__":
    main()
