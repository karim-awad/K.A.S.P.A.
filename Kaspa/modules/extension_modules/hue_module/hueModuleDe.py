from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule


class HueModuleDe(AbstractSubmodule):
    module_name = "Phillips Hue"

    language = "de"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=licht)+.+?(?=chillig)+.': self.action_scene,
                            '((?i).*?(?=licht)+.+?(?=an)+.)|'
                            '((?i).*?(?=licht)+.+?(?=ein)+.)': self.action_on,
                            '((?i).*?(?=ventilator)+.+?(?=ein)+.)': self.action_fan_on,
                            '((?i).*?(?=ventilator)+.+?(?=an)+.)': self.action_fan_on,
                            '((?i).*?(?=warm)+.+?(?=hier)+.)': self.action_fan_on,
                            '((?i).*?(?=ventilator)+.+?(?=aus)+.)': self.action_fan_off,
                            '(?i).*?(?=licht)+.+?(?=aus)+.': self.action_off}

    def action_off(self, query):
        communicator = query.get_communicator()
        self.main_module.off()
        communicator.say("Okay, ich habe das Licht ausgeschalten!")

    def action_on(self, query):
        communicator = query.get_communicator()
        communicator.say("Es werde Licht!")
        self.main_module.on()

    def action_fan_off(self, query):
        communicator = query.get_communicator()
        self.main_module.fan_off()
        communicator.say("Okay, ich habe deinen Ventilator ausgeschalten!")

    def action_fan_on(self, query):
        communicator = query.get_communicator()
        communicator.say("Und er hustete und pustete...")
        self.main_module.fan_on()

    def action_scene(self, query):
        communicator = query.get_communicator()
        self.main_module.scene_relaxing()
        communicator.say('Ok, ich schalte das Licht auf den Entspannungsmodus!')
