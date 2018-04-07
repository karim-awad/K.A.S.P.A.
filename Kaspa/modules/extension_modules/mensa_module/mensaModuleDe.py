from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule


class MensaModuleDe(AbstractSubmodule):
    module_name = "Mensa Erlangen Sued"

    language = "de"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=was)+.+?(?=essen)+.': self.action,
                            '(?i).*?(?=was)+.+?(?=mensa)+.': self.action}

    def action(self, query):
        communicator = query.get_communicator()
        answer = "Heute gibt es folgendes in der Mensa: \n"
        menu = self.main_module.get_menu()
        for i in range(len(menu)):
            answer = answer + menu[i] + "\n"
        recommendation = self.main_module.get_recommendation()
        answer = answer + "Meine Empfehlung wäre das Folgende: " + recommendation
        communicator.say(answer)
