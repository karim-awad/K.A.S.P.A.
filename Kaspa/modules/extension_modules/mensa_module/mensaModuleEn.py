from textblob import TextBlob
from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule


class MensaModuleEn(AbstractSubModule):

    module_name = "Mensa Erlangen Sued"

    language = "en"

    def action(self, query):
        communicator = query.get_communicator()
        answer = "On todays menu are: \n"
        menu = self.main_module.get_menu()
        for i in range(len(menu)):
            tmp = str(TextBlob(menu[i]).translate(from_lang="de", to="en"))
            answer = answer + tmp + "\n"
        recommendation = self.main_module.get_recommendation()
        recommendation = str(TextBlob(recommendation).translate(from_lang="de", to="en"))
        answer = answer + "I'd recommend the " + recommendation
        communicator.say(answer)

    key_regexes = {'(?i).*?(?=what)+.+?(?=on the menu)+.': action}



