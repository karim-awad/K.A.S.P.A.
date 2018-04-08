from Kaspa.modules.abstract_modules.abstractBriefingSubmodule import AbstractBriefingSubmodule


class WeatherModuleEn(AbstractBriefingSubmodule):
    module_name = "Weather"

    language = "en"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=how)+.+?(?=weather)+.+?(?=week)': self.action_week,
                            '(?i).*?(?=how)+.+?(?=weather)+.': self.action_day}

    def action_day(self, query):
        communicator = query.get_communicator()
        icon, summary, temperature_high = self.main_module.daily_forecast(self.language)
        if "clear" in icon or "cloudy" in icon:
            ret = "It is going to be " + summary
        else:
            ret = "There is going to be " + summary
        ret = ret + " The temperature will rise up to " + temperature_high + " degrees Celsius"
        communicator.say(ret)

    def action_week(self, query):
        communicator = query.get_communicator()
        icon, summary = self.main_module.weekly_forecast(self.language)

        if "clear" in icon or "cloudy" in icon:
            ret = "It is going to be " + summary
        else:
            ret = "There is going to be " + summary
        communicator.say(ret)

    def briefing_action(self, query):
        communicator = query.get_communicator()
        icon, summary, temperature_high = self.main_module.daily_forecast(self.language)
        if "clear" in icon or "cloudy" in icon:
            ret = "It is going to be " + summary
        else:
            ret = "There is going to be " + summary
        ret = "Now for today's weather forecast: \n" + \
              ret + " The temperature will rise up to " + temperature_high + " degrees Celsius"
        communicator.say(ret)
