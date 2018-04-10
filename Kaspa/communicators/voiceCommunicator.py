import Kaspa.communicators.resources.snowboy.snowboydecoder as snowboydecoder
# from gtts import gTTS
from Kaspa.assistantCore import AssistantCore
# TODO add resources and make it work
import os
import speech_recognition as sr
from Kaspa.communicators.abstract_communicators.abstractVoiceCommunicator import AbstractVoiceCommunicator
import logging
from Kaspa.config import Config
from Kaspa.communicators.helper.bingTts import BingTts


class VoiceCommunicator(AbstractVoiceCommunicator):
    logger = logging.getLogger("Kaspa")

    # Snowboy config values
    HOTWORD_PATH = "Kaspa/communicators/resources/snowboy/resources/jarvis.pmdl"
    ENERGY_THRESHOLD = 400
    SENSITIVITY = 0.4
    AUDIO_GAIN = 2

    # Volume values
    DECREASED_VOLUME = 50
    INCREASED_VOLUME = 100

    detector = None
    """Hotword detector"""

    recognizer = None
    """Recognizer used for text to speech"""

    language = ''

    def __init__(self):
        super().__init__()
        self.language = Config.get_instance().get("general", "language")

    @staticmethod
    def notify_starting_listening():
        os.system('aplay -q Kaspa/communicators/resources/dong.wav')

    @staticmethod
    def decrease_volume():
        os.system("amixer set PCM " + str(VoiceCommunicator.DECREASED_VOLUME) + "%")

    @staticmethod
    def increase_volume():
        os.system("amixer set PCM " + str(VoiceCommunicator.INCREASED_VOLUME) + "%")

    @staticmethod
    def notify_finished_listening():
        os.system('aplay -q Kaspa/communicators/resources/ding.wav')

    @staticmethod
    def notify_error():
        os.system('aplay -q Kaspa/communicators/resources/dong.wav')

    def say(self, text):
        # self.logger.info("Jarvis said: " + text)
        # tts = gTTS(text=text, lang=self.language)
        # tts.save("/tmp/.kaspaAnswer.mp3")
        # os.system("mpg123 -q /tmp/.kaspaAnswer.mp3")
        language = self.language
        if self.language is 'en':
            language = "en-US"
        print(text)
        BingTts().tts(text, language)

    def ask(self, text):
        self.say(text)
        answer = self.record()
        self.logger.info("User answered: " + answer)
        return answer

    def record(self):
        """ listen for user input
            @return string, the user answered"""
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
            language = self.language
            if self.language is 'en':
                language = "en-US"
            query = self.recognizer.recognize_google(audio, language=language)
            self.logger.info("User said " + query)
            return query

    def detected_callback(self):
        """gets called when wakeword detection recognizes wakeword"""
        core = AssistantCore()
        self.logger.info("hotword detected")
        self.detector.terminate()
        self.notify_starting_listening()
        self.decrease_volume()
        try:
            command = self.record()
        except sr.UnknownValueError:
            self.logger.info("Could not hear anything")
            self.say("Sorry, but I could not hear anything")
            self.detector.start(self.detected_callback)
            return
        except sr.RequestError as e:
            self.logger.error("Could not request results" + str(e))
            self.say("Sorry, but I could not request results")
            self.detector.start(self.detected_callback)
            return
        except Exception as e:
            self.logger.error(str(e))
            self.say("Sorry, but I didn't understand that.")
            self.detector.start(self.detected_callback)
            return
        self.increase_volume()
        self.notify_finished_listening()
        core.answer(self, command)
        self.logger.info("listening")
        self.detector.start(self.detected_callback)

    def run(self):
        """listens offline for the wakeword, then calls detected_callback"""
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = self.ENERGY_THRESHOLD

        self.logger.info("Voice communicator is listening...")
        self.detector = snowboydecoder.HotwordDetector(self.HOTWORD_PATH, sensitivity=self.SENSITIVITY,
                                                       audio_gain=self.AUDIO_GAIN)
        self.detector.start(self.detected_callback)
