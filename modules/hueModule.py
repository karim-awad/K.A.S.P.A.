import phue
from phue import Bridge
from modules.helper import ifttt
from abstractModule import AbstractModule
from config import Config
from moduleException import ModuleException


class HueModule(AbstractModule):
    key_regexes = ['(?i).*?(?=set)+.+?(?=light)+.', '(?i).*?(?=turn)+.+?(?=light)+.']
    module_name = 'Phillips Hue'

    config_parameters = {"bridge_ip": "Enter the ip adress of your Philips Hue Bridge here. Make sure, that you have"
                                      " pressed the button on the bridge before hitting enter."}

    b = None

    def configure(self):
        try:
            bridge_ip = Config.get_instance().get("hue", "bridge_ip")
            self.b = Bridge(bridge_ip)
        except phue.PhueRegistrationException:
            raise ModuleException(self.module_name, "Philips Hue Bridge Button not pressed!")

    def off(self):
        self.b.set_group(1, 'on', False)

    def on(self):
        self.b.set_group(1, 'on', True)

    def scene(self, chosen_scene):
        assert chosen_scene in ["chillig"]
        if chosen_scene is "chillig":
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
