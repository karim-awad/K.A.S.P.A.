from langdetect import language

from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule
from datetime import datetime
from Kaspa.config import Config
import googlemaps


class GoogleMapsModuleEn(AbstractSubmodule):
    module_name = "Google Maps"

    language = "en"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=navigate)+.': self.action}

    def get_simple_transit(self, start, stop):
        now = datetime.now()

        directions = self.main_module.google_maps.directions(
            start, stop, mode="transit", departure_time=now, language=self.language)

        legs = directions[0]["legs"]
        transit_instructions = list()
        vehicles = list()
        for leg in legs:
            steps = leg["steps"]
            for step in steps:

                if step["travel_mode"] == "WALKING":
                    substeps = step["steps"]
                    for substep in substeps:
                        pass

                if step["travel_mode"] == "TRANSIT":
                    departure_time = step["transit_details"][
                        "departure_time"]["text"]
                    departure_stop = step["transit_details"][
                        "departure_stop"]["name"]
                    instructions = step["html_instructions"]
                    transit_instructions.append(
                        "At " +
                        departure_time +
                        " from " +
                        departure_stop +
                        " take the " +
                        instructions)
                    vehicles.append(
                                    step["transit_details"]["line"]["vehicle"]
                                    ["name"] + " " +
                                    step["transit_details"]["line"]
                                    ["short_name"])

        spoken_vehicles = "All in all this includes taking the "
        for vehicle in vehicles:
            spoken_vehicles
            if vehicles.index(vehicle) is 0:
                spoken_vehicles = spoken_vehicles + vehicle
            elif vehicles.index(vehicle) is len(vehicles) - 1:
                spoken_vehicles = spoken_vehicles + " and the " + vehicle
            else:
                spoken_vehicles = spoken_vehicles + ", the " + vehicle

        if len(transit_instructions) == 1:
            return transit_instructions[0]
        return transit_instructions[0] + ". " + spoken_vehicles + "."

    def action(self, query):
        query_text = query.get_text()
        communicator = query.get_communicator()
        config = Config.get_instance()
        home = config.get('locations', 'home')
        locations = config.get_section_content('locations')
        for location in locations:
            if location[0] in query_text:
                communicator.say(self.get_simple_transit(home, location[1]))
                return
        communicator.say("Sorry, I don't know that location")
