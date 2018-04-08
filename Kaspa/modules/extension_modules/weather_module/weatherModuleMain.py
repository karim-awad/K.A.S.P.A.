import forecastio
from Kaspa.modules.abstract_modules.abstractBriefingModule import AbstractBriefingModule
from Kaspa.modules.extension_modules.weather_module.weatherModuleEn import WeatherModuleEn
from Kaspa.modules.extension_modules.weather_module.weatherModuleDe import WeatherModuleDe
from Kaspa.config import Config


class WeatherModuleMain(AbstractBriefingModule):
    module_name = "Weather"

    config_parameters = {"api_key": "This is the DarkSky Weather Api key. You can get it for free from here: \n"
                                    "https://darksky.net/dev \n",
                         "latitude": "The latitude of your location",
                         "longitude": "The longitude of your location"}

    api_key = None
    lat = None
    lng = None

    def __init__(self):
        super(WeatherModuleMain, self).__init__()
        self.add_submodule(WeatherModuleDe())
        self.add_submodule(WeatherModuleEn())

    def configure(self):
        config = Config.get_instance()
        self.api_key = config.get('weather', 'api_key')
        self.lat = config.get('weather', 'latitude')
        self.lng = config.get('weather', 'longitude')

    def daily_forecast(self, language):
        forecast = forecastio.load_forecast(self.api_key, self.lat, self.lng, lang=language)
        datablock = forecast.hourly()
        datablock_daily = forecast.daily()
        summary = datablock.summary
        icon = datablock.icon
        datapoint = datablock_daily.data[0]
        return icon, summary, str(int(datapoint.temperatureHigh))

    def weekly_forecast(self, language):
        forecast = forecastio.load_forecast(self.api_key, self.lat, self.lng, lang=language)
        datablock_daily = forecast.daily()
        summary = datablock_daily.summary
        icon = datablock_daily.icon

        return icon, summary
