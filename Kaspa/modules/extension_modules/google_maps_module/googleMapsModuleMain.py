import googlemaps
from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.config import Config
from Kaspa.modules.extension_modules.google_maps_module.googleMapsModuleDe import GoogleMapsModuleDe
from Kaspa.modules.extension_modules.google_maps_module.googleMapsModuleEn import GoogleMapsModuleEn


class GoogleMapsModuleMain(AbstractModule):

    module_name = "Google Maps"

    config_parameters = {"google_maps": "This is you Google Maps API key. You can get it here:\n"
                                        "https://developers.google.com/maps/documentation/javascript/get-api-key?hl"
                                        "=en#key"}

    google_maps = None

    def __init__(self):
        super(GoogleMapsModuleMain, self).__init__()
        self.add_submodule(GoogleMapsModuleEn())
        self.add_submodule(GoogleMapsModuleDe())

    def configure(self):
        api_key = Config.get_instance().get("google maps", "api_key")
        self.google_maps = googlemaps.Client(key=api_key)


