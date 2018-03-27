import forecastio
from modules.abstract_modules.abstractBriefingModule import AbstractBriefingModule
from config import Config


class WeatherModule(AbstractBriefingModule):
    key_regexes = ['(?i).*?(?=how)+.+?(?=weather)+.']

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

    def get_day(self):
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
        return ret

    def get_week(self):
        forecast = forecastio.load_forecast(self.api_key, self.lat, self.lng)
        datablock_daily = forecast.daily()
        summary = datablock_daily.summary
        icon = datablock_daily.icon
        if "clear" in icon or "cloudy" in icon:
            ret = "It is going to be " + summary
        else:
            ret = "There is going to be " + summary
        return ret

    def briefing_action(self, query):
        query.get_communicator().say(self.get_day())

    def action(self, query):
        communicator = query.get_communicator()
        text = query.get_text()
        if "week" in text:
            communicator.say(self.get_week())
        else:
            communicator.say(self.get_day())
