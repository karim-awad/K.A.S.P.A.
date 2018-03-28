import resources.snowboy.snowboydecoder as snowboydecoder
from gtts import gTTS
from Kaspa import assistantCore
# TODO add resources and make it work
import os
import speech_recognition as sr
from Kaspa.communicators.abstract_communicators.abstractVoiceCommunicator import AbstractVoiceCommunicator
import logging


class VoiceCommunicator(AbstractVoiceCommunicator):
    logger = logging.getLogger("Kaspa")

    # Snowboy config values
    HOTWORD_PATH = "resources/snowboy/resources/jarvis.pmdl"
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

    @staticmethod
    def notify_starting_listening():
        os.system('aplay -q resources/dong.wav')

    @staticmethod
    def decrease_volume():
        os.system("amixer set PCM " + str(VoiceCommunicator.DECREASED_VOLUME) + "%")

    @staticmethod
    def increase_volume():
        os.system("amixer set PCM " + str(VoiceCommunicator.INCREASED_VOLUME) + "%")

    @staticmethod
    def notify_finished_listening():
        os.system('aplay -q resources/ding.wav')

    @staticmethod
    def notify_error():
        os.system('aplay -q resources/dong.wav')

    def answer(self, query):
        assistantCore.answer(self, query)

    def say(self, text):
        self.logger.info("Jarvis said: " + text)
        tts = gTTS(text=text, lang='en')
        tts.save("resources/answers/answer.mp3")
        os.system("mpg123 -q resources/answers/answer.mp3")

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
        try:
            query = self.recognizer.recognize_google(audio)
            self.logger.info("User said " + query)
            return query
        except sr.UnknownValueError:
            self.logger.info("Could not hear anything")
        except sr.RequestError as e:
            self.logger.error("Could not request results" + str(e))
        except Exception as e:
            self.logger.error(str(e))
        finally:
            self.increase_volume()
            self.notify_error()
            return ''

    def detected_callback(self):
        """gets called when wakeword detection recognizes wakeword"""
        self.logger.info("hotword detected")
        self.detector.terminate()
        self.notify_starting_listening()
        self.decrease_volume()
        command = self.record()
        self.answer(command)
        self.increase_volume()
        self.logger.info("listening")
        self.detector.start(self.detected_callback)

    def start_conversation(self):
        """listens offline for the wakeword, then calls detected_callback"""
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = self.ENERGY_THRESHOLD

        self.logger.info("Voice communicator is listening...")
        self.detector = snowboydecoder.HotwordDetector(self.HOTWORD_PATH, sensitivity=self.SENSITIVITY,
                                                       audio_gain=self.AUDIO_GAIN)
        self.detector.start(self.detected_callback)
