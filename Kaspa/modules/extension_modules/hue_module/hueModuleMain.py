import phue
from phue import Bridge
from Kaspa.modules.extension_modules.helper import ifttt
from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.extension_modules.hue_module.hueModuleDe import HueModuleDe
from Kaspa.modules.extension_modules.hue_module.hueModuleEn import HueModuleEn
from Kaspa.config import Config
from Kaspa.modules.exceptions.impossibleActionError import ImpossibleActionError
from Kaspa.modules.exceptions.moduleError import ModuleError


class HueModuleMain(AbstractModule):

    module_name = 'Phillips Hue'

    config_parameters = {"bridge_ip": "Enter the ip address of your Philips Hue Bridge here. Make sure, that you have"
                                      " pressed the button on the bridge before hitting enter."}

    bridge = None

    def __init__(self):
        super(HueModuleMain, self).__init__()
        self.add_submodule(HueModuleDe())
        self.add_submodule(HueModuleEn())

    def configure(self):
        try:
            bridge_ip = Config.get_instance().get("hue", "bridge_ip")
            self.bridge = Bridge(bridge_ip)
        except phue.PhueRegistrationException:
            # TODO figure out how to localize error message here
            raise ImpossibleActionError("You have to press the button on your bridge first!")
        except Exception as e:
            raise ModuleError(self.module_name, str(e))

    @staticmethod
    def scene(chosen_scene):
        assert chosen_scene in ["chillig"]
        if chosen_scene is "chillig":
            # the event has to be created on ifttt.com first
            ifttt.send_event("huescene")

    def off(self):
        try:
            self.bridge.set_group(1, 'on', False)
        except phue.PhueRequestTimeout:
            raise ImpossibleActionError("Connection timed out.")
        except Exception as e:
            raise ModuleError(self.module_name, str(e))

    def on(self):
        try:
            self.bridge.set_group(1, 'on', True)
        except phue.PhueRequestTimeout:
            raise ImpossibleActionError("Connection timed out.")
        except Exception as e:
            raise ModuleError(self.module_name, str(e))

    # maybe going to switch to selection of more scenes, but it is good enough for my usage right now
    def scene_relaxing(self):
        self.scene('chillig')
