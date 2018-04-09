from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule
from datetime import datetime
from Kaspa.config import Config


class GoogleMapsModuleDe(AbstractSubmodule):
    module_name = "Google Maps"

    language = "de"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=navigiere)+.': self.action,
                            '((?i).*?(?=wie)+.+?(?=komme)+.+?(?=ich)+.)': self.action}

    def get_transit(self, start, stop):
        now = datetime.now()

        directions = self.main_module.google_maps.directions(
            start, stop, mode="transit", departure_time=now, language=self.language)

        legs = directions[0]["legs"]
        transit_instructions = ""
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
                    artikel = " die "
                    if "Bus" in instructions or "zug" in instructions:
                        artikel = " den "
                    transit_instructions = transit_instructions + "Nehme um " + departure_time + " an der Station " + \
                                           departure_stop + artikel + instructions + " bis zur Station " \
                                           + arrival_stop + ". "

        return transit_instructions

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
                    artikel = " die "
                    if "Bus" in instructions or "zug" in instructions:
                        artikel = " den "

                    transit_instructions.append(
                        "Nehme um " +
                        departure_time +
                        " an der Station " +
                        departure_stop +
                        artikel +
                        instructions)
                    vehicles.append(
                        step["transit_details"]["line"]["vehicle"]
                        ["name"] + " " +
                        step["transit_details"]["line"]
                        ["short_name"])

        spoken_vehicles = "Alles in allem musst du dabei "
        for vehicle in vehicles:
            artikel = "die "
            if "Bus" in vehicle or "zug" in vehicle:
                artikel = "den "
            if vehicles.index(vehicle) is 0:
                spoken_vehicles = spoken_vehicles + artikel + vehicle
            elif vehicles.index(vehicle) is len(vehicles) - 1:
                spoken_vehicles = spoken_vehicles + " und " + artikel + vehicle
            else:
                spoken_vehicles = spoken_vehicles + ", " + artikel + vehicle

        if len(transit_instructions) == 1:
            return transit_instructions[0]
        return transit_instructions[0] + ". " + spoken_vehicles + " nehmen."

    def action(self, query):
        query_text = query.get_text()
        communicator = query.get_communicator()
        config = Config.get_instance()
        home = config.get('locations', 'home')
        # search for saved location in config
        locations = config.get_section_content('locations')
        for location in locations:
            if location[0] in query_text:
                # location is in shortcuts => show simple transit
                communicator.say(self.get_simple_transit(home, location[1]))
                return
        location = communicator.ask("Der Ort befindet sich nicht unter deinen gespeicherten Orten. "
                                    "\n Kannst du ihn bitte nocheinmal wiederholen?")
        # new location => show full transit
        communicator.say(self.get_transit(home, location))
