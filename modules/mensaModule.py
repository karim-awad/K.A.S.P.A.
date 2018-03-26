import urllib.request
from textblob import TextBlob
from bs4 import BeautifulSoup as Bs
from abstractModule import AbstractModule


class MensaModule(AbstractModule):

    key_regexes = ['(?i).*?(?=what)+.+?(?=on the menu)+.']

    module_name = "Mensa Erlangen Sued"

    def parse_umlaute(self, string):
        for i in range(len(string)):
            if string[i:i+6] == "&auml;":
                string = string[:i] + "ä" + string[i+6:]
            if string[i:i+6] == "&ouml;":
                string = string[:i] + "ö" + string[i+6:]
            if string[i:i+6] == "&uuml;":
                string = string[:i] + "ü" + string[i+6:]
            if string[i:i+6] == "&quot;":
                string = string[:i] + '"' + string[i+6:]
            if string[i:i+8] == "&ntilde;":
                string = string[:i] + 'ñ' + string[i+8:]
        return string

    def get_menu(self):
        url = "https://www.sigfood.de/?do=api.gettagesplan"

        response = urllib.request.urlopen(url).read()
        soup = Bs(response, features="xml")

        gerichte = soup.findAll("hauptgericht")
        menu = list()
        for i in range(len(gerichte)):
            food = self.parse_umlaute(gerichte[i].bezeichnung.string)
            menu.append(str(TextBlob(food).translate(from_lang="de", to="en")))
        return menu

    def get_recommendation(self):
        url = "https://www.sigfood.de/?do=api.gettagesplan"

        response = urllib.request.urlopen(url).read()
        soup = Bs(response, features="xml")
        menu = list()
        rating = list()
        halal = soup.findAll(moslem='true') + soup.findAll(vegetarisch='true')
        for food in halal:
            gerichte = food.findAll("hauptgericht")
            for i in range(len(gerichte)):
                food = self.parse_umlaute(gerichte[i].bezeichnung.string)
                rating.append(float(gerichte[i].bewertung.schnitt.string))
                menu.append(str(TextBlob(food).translate(from_lang="de", to="en")))

        max_rating = 0
        max_index = 0
        for i in range(len(rating)):
            if rating[i] > max_rating:
                max_rating = rating[i]
                max_index = i
        return menu[max_index]

    def action(self, query):
        communicator = query.get_communicator()
        answer = "On todays menu are: \n"
        menu = self.get_menu()
        for i in range(len(menu)):
            answer = answer + menu[i] + "\n"
        recommendation = self.get_recommendation()
        answer = answer + "I'd recommend the " + recommendation
        communicator.say(answer)


