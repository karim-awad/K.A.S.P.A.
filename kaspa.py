#!/usr/bin/env python3.6
import logging
import os
import subprocess
import signal
from Kaspa.config import Config
from pathlib import Path
import Kaspa.strings.strings as strings

from Kaspa.modules.core_modules.daily_briefing_module.dailyBriefingModuleMain import DailyBriefingModuleMain
from Kaspa.modules.core_modules.example_command_module.exampleCommandModuleMain import ExampleCommandModuleMain
from Kaspa.modules.core_modules.conversation_module.conversationModuleMain import ConversationModuleMain
from Kaspa.modules.extension_modules.hue_module.hueModuleMain import HueModuleMain
from Kaspa.modules.extension_modules.weather_module.weatherModuleMain import WeatherModuleMain
from Kaspa.modules.extension_modules.tv_guide_module.tvGuideModuleMain import TvGuideModuleMain
from Kaspa.modules.extension_modules.google_maps_module.googleMapsModuleMain import GoogleMapsModuleMain
from Kaspa.modules.extension_modules.news_module.newsModuleMain import NewsModuleMain
from Kaspa.modules.extension_modules.mensa_module.mensaModuleMain import MensaModuleMain
from Kaspa.modules.extension_modules.reddit_module.redditModuleMain import RedditModuleMain
from Kaspa.modules.extension_modules.time_module.timeModuleMain import TimeModuleMain
from Kaspa.modules.extension_modules.spotify_module.spotifyModuleMain import SpotifyModuleMain
from Kaspa.modules.extension_modules.knowledge_module.knowledgeModuleMain import KnowledgeModuleMain

from Kaspa.modules.exceptions.moduleError import ModuleError

from Kaspa.communicators.voiceCommunicator import VoiceCommunicator
from Kaspa.communicators.telegramCommunicator import TelegramCommunicator
from Kaspa.communicators.commandlineCommunicator import CommandlineCommunicator

logger = None


def init_modules():
    """initializes the wanted modules"""
    try:
        DailyBriefingModuleMain().activate()

        ExampleCommandModuleMain().activate()

        ConversationModuleMain().activate()

        SpotifyModuleMain().activate()

        GoogleMapsModuleMain().activate()

        HueModuleMain().activate()

        TimeModuleMain().activate()

        TvGuideModuleMain().activate()

        MensaModuleMain().activate()

        RedditModuleMain().activate()

        WeatherModuleMain().activate()

        NewsModuleMain().activate()

        KnowledgeModuleMain().activate()

    except ModuleError as e:
        logger.error(e.message())
        print(e.message())
        exit(1)


def start_communicators():
    """starts all wanted communicators"""
    vc = VoiceCommunicator()
    #clc = CommandlineCommunicator()
    tc = TelegramCommunicator()

    tc.start()
    #clc.start()
    vc.start()


def sigint_handler(signal, frame):
    # load strings for this module
    static_strings = strings.get_strings("kaspa")
    print(static_strings["GOODBYE"])
    exit(0)


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

    # Initialize signal handling for Sigint
    signal.signal(signal.SIGINT, sigint_handler)

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
