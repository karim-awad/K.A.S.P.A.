import logging
import os
import subprocess
from config import Config
from pathlib import Path
from modules.core_modules.dailyBriefingModule import DailyBriefingModule
from modules.core_modules.conversationModule import ConversationModule
from modules.core_modules.exampleCommandModule import ExampleCommandModule
from modules.extension_modules.googleMapsModule import GoogleMapsModule
from modules.extension_modules.hueModule import HueModule
from modules.extension_modules.newsModule import NewsModule
from modules.extension_modules.redditModule import RedditModule
from modules.extension_modules.mensaModule import MensaModule
from modules.core_modules.timeModule import TimeModule
from modules.extension_modules.weatherModule import WeatherModule
from modules.extension_modules.spotifyModule import SpotifyModule
from modules.extension_modules.wikipediaModule import WikipediaModule
from modules.extension_modules.wolframAlphaModule import WolframAlphaModule

from modules.moduleException import ModuleException

# from voiceCommunicator import VoiceCommunicator
from communicators.commandlineCommunicator import CommandlineCommunicator

logger = None


def init_modules():
    """initializes the wanted modules"""
    try:
        daily_briefing_module = DailyBriefingModule()
        daily_briefing_module.activate()

        example_command_module = ExampleCommandModule()
        example_command_module.activate()

        conversation_module = ConversationModule()
        conversation_module.activate()

        spotify_module = SpotifyModule()
        spotify_module.activate()

        google_maps_module = GoogleMapsModule()
        google_maps_module.activate()

        hue_module = HueModule()
        hue_module.activate()

        time_module = TimeModule()
        time_module.activate()

        mensa_module = MensaModule()
        mensa_module.activate()

        reddit_module = RedditModule()
        reddit_module.activate()

        weather_module = WeatherModule()
        weather_module.activate()

        news_module = NewsModule()
        news_module.activate()

        wikipedia_module = WikipediaModule()
        wikipedia_module.activate()

        wolfram_alpha_module = WolframAlphaModule()
        wolfram_alpha_module.activate()

        # TODO get modules from config

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
    Config.get_instance().load_modules()

    # Start mopidy server
    devnull = open(os.devnull, 'w')
    logger.info("Starting mopidy server...")
    subprocess.call("killall mopidy", shell=True, stderr=devnull, stdout=devnull, stdin=devnull)
    subprocess.call("mopidy -q &", shell=True, stderr=devnull, stdout=devnull, stdin=devnull)
    logger.info("Mopidy server started")

    # start communicators
    logger.info("Starting Communicators...")
    start_communicators()


if __name__ == "__main__":
    main()
