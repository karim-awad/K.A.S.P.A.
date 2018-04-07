from telegram.ext import Updater
import logging
import telegram
import speech_recognition as sr
from threading import Semaphore
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import BaseFilter
from Kaspa.config import Config
from Kaspa.communicators.abstract_communicators.abstractTextCommunicator import AbstractTextCommunicator
import os

from Kaspa.assistantCore import AssistantCore


class TelegramCommunicator(AbstractTextCommunicator):
    api_key = ''
    chat_id = ''

    thread_sync = dict()
    """dict of chatid to thread sync object"""

    communicators = dict()
    """dict of all active communicators"""

    class Filter(BaseFilter):

        def filter(self, message):
            if message.text is not None:
                return True
            if message.voice is not None:
                return True
            return False

    class ThreadSync(object):
        sem = None

        waiting = False
        """bool that shows whether thread is waiting for answer"""

        question_answer = ''
        """bot puts the answer of a question here if thread is waiting for it"""

        def __init__(self):
            self.sem = Semaphore(0)
            self.waiting = False
            self.question_answer = ''

    class __TelegramCommunicator(AbstractTextCommunicator):

        api_key = ''
        chat_id = ''
        bot = None
        update = None

        AUDIO_FILE = "/tmp/.voice.wav"
        TEMP_AUDIO_FILE = "/tmp/.voice.ogg"

        def __init__(self, chat_id, bot, update):
            super().__init__(class_name="TelegramCommunicator")
            self.api_key = Config.get_instance().get('telegram', 'api_key')
            self.chat_id = chat_id
            self.bot = bot
            self.update = update

        def say(self, text):
            self.bot.send_message(chat_id=self.chat_id, text=text)

        def ask(self, question):
            self.bot.send_message(chat_id=self.chat_id, text=question)
            TelegramCommunicator.thread_sync[self.chat_id].waiting = True
            TelegramCommunicator.thread_sync[self.chat_id].sem.acquire(blocking=True)
            TelegramCommunicator.thread_sync[self.chat_id].waiting = False
            return TelegramCommunicator.thread_sync[self.chat_id].question_answer

        def stt(self):
            r = sr.Recognizer()
            with sr.AudioFile(self.AUDIO_FILE) as source:
                audio = r.record(source)  # read the entire audio file
                language = Config.get_instance().get("general", "language")
                return r.recognize_google(audio, language=language)

        def send_image(self, bot, chat_id, image):
            bot.send_photo(chat_id=self.chat_id, photo=open(image, 'rb'))

        def run(self):
            """reacts to text messages"""
            bot = self.bot
            update = self.update
            bot.send_chat_action(chat_id=self.chat_id, action=telegram.ChatAction.TYPING)
            text = update.message.text

            if update.message.voice is not None:
                """voice message received"""
                file = bot.getFile(update.message.voice.file_id)
                file.download(self.TEMP_AUDIO_FILE)
                os.system("opusdec " + self.TEMP_AUDIO_FILE + " " + self.AUDIO_FILE)
                os.system("rm -rf " + self.TEMP_AUDIO_FILE)
                try:
                    self.stt()
                except sr.UnknownValueError:
                    self.say(self.strings["NO_UNDERSTANDING"])
                    return
                except sr.RequestError as e:
                    self.say(self.strings["IMPOSSIBLE_REQUEST"])
                    return
                core = AssistantCore()
                core.answer(self, self.stt())
                return

            core = AssistantCore()
            core.answer(self, text)

    def start_command(self, bot, update):
        """gets called when /start command is received"""
        chatid = update.message.chat_id
        if self.is_authorized(chatid):
            bot.send_message(chat_id=chatid, text=self.strings["START_AUTHORIZED"])
        else:
            bot.send_message(chat_id=chatid, text=self.strings["START_UNAUTHORIZED"])

    def is_authorized(self, chat_id):
        return str(chat_id) == self.chat_id

    def __init__(self):
        super().__init__()
        self.api_key = Config.get_instance().get('telegram', 'api_key')
        self.chat_id = Config.get_instance().get('telegram', 'chat_id')

    def answer(self, bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)

        if not self.is_authorized(update.message.chat_id):
            """check if chat partner is authorized"""
            bot.send_message(chat_id=update.message.chat_id, text=self.strings["START_UNAUTHORIZED"])
            return

        if update.message.chat_id in TelegramCommunicator.thread_sync.keys() \
                and TelegramCommunicator.thread_sync[update.message.chat_id].waiting:
            """check if thread is currently waiting for an answer to a question,
                if so write received message into the sync object and notify the thread that the answer is there"""
            TelegramCommunicator.thread_sync[update.message.chat_id].question_answer = update.message.text
            TelegramCommunicator.thread_sync[update.message.chat_id].sem.release()
        else:
            """create new thread"""
            TelegramCommunicator.thread_sync[update.message.chat_id] = TelegramCommunicator.ThreadSync()
            communicator = self.__TelegramCommunicator(update.message.chat_id, bot, update)
            self.communicators[update.message.chat_id] = communicator
            communicator.start()

    def run(self):
        updater = Updater(token=self.api_key)
        dispatcher = updater.dispatcher

        filter_audiotext = self.Filter()
        start_handler = CommandHandler('start', self.start_command)
        kaspa_handler = MessageHandler(filter_audiotext, self.answer)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(kaspa_handler)

        updater.start_polling()
