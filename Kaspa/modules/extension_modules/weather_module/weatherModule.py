import forecastio
from Kaspa.modules.abstract_modules.abstractBriefingModule import AbstractBriefingModule
from Kaspa.config import Config


class WeatherModule(AbstractBriefingModule):
    module_name = "Weather"

    config_parameters = {"api_key": "This is the DarkSky Weather Api key. You can get it for free from here: \n"
                                    "https://darksky.net/dev \n",
                         "latitude": "The latitude of your location",
                         "longitude": "The longitude of your location"}

    api_key = None
    lat = None
    lng = None

    def configure(self):
        config = Config.get_instance()
        self.api_key = config.get('weather', 'api_key')
        self.lat = config.get('weather', 'latitude')
        self.lng = config.get('weather', 'longitude')

    def action_day(self, query):
        communicator = query.get_communicator()
        forecast = forecastio.load_forecast(self.api_key, self.lat, self.lng)
        datablock = forecast.hourly()
        datablock_daily = forecast.daily()
        summary = datablock.summary
        icon = datablock.icon
        ret = ""
        if "clear" in icon or "cloudy" in icon:
            ret = "It is going to be " + summary
        else:
            ret = "There is going to be " + summary
        datapoint = datablock_daily.data[0]
        ret = ret + " The temperature will rise up to " + str(int(datapoint.temperatureHigh)) + " degrees Celsius"
        communicator.say(ret)

    def action_week(self, query):
        communicator = query.get_communicator()
        forecast = forecastio.load_forecast(self.api_key, self.lat, self.lng)
        datablock_daily = forecast.daily()
        summary = datablock_daily.summary
        icon = datablock_daily.icon
        if "clear" in icon or "cloudy" in icon:
            ret = "It is going to be " + summary
        else:
            ret = "There is going to be " + summary
        communicator.say(ret)

    def briefing_action(self, query):
        query.get_communicator().say("Now the weather: ")
        self.action_day(query)

    key_regexes = {'(?i).*?(?=how)+.+?(?=weather)+.+?(?=week)': action_day,
                   '(?i).*?(?=how)+.+?(?=weather)+.': action_week}