from modules.abstract_modules.abstractBriefingModule import AbstractBriefingModule
import time


class TimeModule(AbstractBriefingModule):

    key_regexes = ['(?i).*?(?=what)+.+?(?=time)+.']

    module_name = "Time"

    def action(self, query):
        communicator = query.get_communicator()
        communicator.say("It is " + time.strftime("%H:%M"))
