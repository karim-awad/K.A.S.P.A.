from Kaspa.modules.abstract_modules.abstractBriefingSubmodule import AbstractBriefingSubmodule


class WeatherModuleDe(AbstractBriefingSubmodule):
    module_name = "Weather"

    language = "de"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=wie)+.+?(?=wetter)+.+?(?=woche)': self.action_week,
                            '(?i).*?(?=wie)+.+?(?=wetter)+.': self.action_day}

    def action_day(self, query):
        communicator = query.get_communicator()
        icon, summary, temperature_high = self.main_module.daily_forecast(self.language)
        # if "clear" in icon or "cloudy" in icon:
        #     ret = "Es wird " + summary
        # else:
        #     ret = "Es kommt " + summary
        ret = summary + " Die Temperatur steigt voraussichtlich bis auf " + temperature_high + " Grad an."
        communicator.say(ret)

    def action_week(self, query):
        communicator = query.get_communicator()
        icon, summary = self.main_module.weekly_forecast(self.language)

        # if "clear" in icon or "cloudy" in icon:
        #     ret = "Es wird " + summary
        # else:
        #     ret = "Es erwartet dich " + summary
        communicator.say(summary)

    def briefing_action(self, query):
        communicator = query.get_communicator()
        icon, summary, temperature_high = self.main_module.daily_forecast(self.language)
        ret = "Jetzt folgt der heutige Wetterbericht: \n" + summary + \
              " Die Temperatur steigt voraussichtlich bis auf " + temperature_high + " Grad an."
        communicator.say(ret)