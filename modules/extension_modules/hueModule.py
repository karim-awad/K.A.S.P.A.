import phue
from phue import Bridge
from modules.extension_modules.helper import ifttt
from modules.abstract_modules.abstractModule import AbstractModule
from config import Config
from modules.moduleException import ModuleException


class HueModule(AbstractModule):
    key_regexes = ['(?i).*?(?=set)+.+?(?=light)+.', '(?i).*?(?=turn)+.+?(?=light)+.']
    module_name = 'Phillips Hue'

    config_parameters = {"bridge_ip": "Enter the ip adress of your Philips Hue Bridge here. Make sure, that you have"
                                      " pressed the button on the bridge before hitting enter."}

    bridge = None

    def configure(self):
        try:
            bridge_ip = Config.get_instance().get("hue", "bridge_ip")
            self.bridge = Bridge(bridge_ip)
        except phue.PhueRegistrationException:
            raise ModuleException(self.module_name, "Philips Hue Bridge Button not pressed!")

    def off(self):
        self.bridge.set_group(1, 'on', False)

    def on(self):
        self.bridge.set_group(1, 'on', True)

    @staticmethod
    def scene(chosen_scene):
        assert chosen_scene in ["chillig"]
        if chosen_scene is "chillig":
            # the event has to be created on ifttt.com first
            ifttt.send_event("huescene")

    def action(self, query):
        query_text = query.get_text()
        communicator = query.get_communicator()

        if 'turn' in query_text:
            if 'on' in query_text:
                self.on()
            else:
                self.off()

        if 'set' in query_text:
            if 'relaxing' in query_text:
                self.scene('chillig')
        communicator.say('Ok, done!')
