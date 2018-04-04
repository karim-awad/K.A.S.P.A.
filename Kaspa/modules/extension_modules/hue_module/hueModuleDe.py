from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule


class HueModuleDe(AbstractSubModule):

    module_name = "Phillips Hue"

    language = "de"

    def action_off(self, query):
        communicator = query.get_communicator()
        self.main_module.off()
        communicator.say("Okay, ich habe das Licht ausgeschalten!")

    def action_on(self, query):
        communicator = query.get_communicator()
        communicator.say("Es werde Licht!")
        self.main_module.on()

    def action_scene(self, query):
        communicator = query.get_communicator()
        self.main_module.scene_relaxing()
        communicator.say('Ok, ich schalte das Licht auf den Entspannungsmodus!')

    key_regexes = {'(?i).*?(?=licht)+?(?=entspannung)+.': action_scene,
                   '((?i).*(?=licht)+.+?(?=an)+.)|'
                   '((?i).*?(?=licht)+.+?(?=ein)+.)': action_on,
                   '((?i).*?(?=licht)+.+?(?=aus)+.)': action_off}
