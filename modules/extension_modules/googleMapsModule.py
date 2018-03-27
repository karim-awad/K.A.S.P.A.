import googlemaps
from datetime import datetime
from modules.abstract_modules.abstractModule import AbstractModule
from config import Config


class GoogleMapsModule(AbstractModule):

    key_regexes = ['(?i).*?(?=navigate)+.']

    module_name = "Google Maps"

    config_parameters = {"google_maps": "This is you Google Maps API key. You can get it here:\n" \
                                        "https://developers.google.com/maps/documentation/javascript/get-api-key?hl"
                                        "=en#key"}

    google_maps = None

    def configure(self):
        api_key = Config.get_instance().get("google maps", "api_key")
        self.google_maps = googlemaps.Client(key=api_key)

    @staticmethod
    def get_transit(start, stop):
        now = datetime.now()

        directions = GoogleMapsModule.google_maps.directions(
            start, stop, mode="transit", departure_time=now)

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
                    arrival_stop = step["transit_details"]["arrival_stop"]["name"]
                    instructions = step["html_instructions"]
                    transit_instructions.append(
                        "At " +
                        departure_time +
                        " from " +
                        departure_stop +
                        " take the " +
                        instructions +
                        " until " +
                        arrival_stop)
                    vehicles.append(
                                    step["transit_details"]["line"]["vehicle"]
                                    ["name"] + " " +
                                    step["transit_details"]["line"]
                                    ["short_name"])

        return transit_instructions

    @staticmethod
    def get_simple_transit(start, stop):
        now = datetime.now()

        directions = GoogleMapsModule.google_maps.directions(
            start, stop, mode="transit", departure_time=now)

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


