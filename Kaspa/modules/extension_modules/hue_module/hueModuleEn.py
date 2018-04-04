from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubModule


class HueModuleEn(AbstractSubModule):

    module_name = "Phillips Hue"

    language = "en"

    def action_off(self, query):
        communicator = query.get_communicator()
        self.main_module.off()
        communicator.say("Okay, lights turned off!")

    def action_on(self, query):
        communicator = query.get_communicator()
        self.main_module.on()
        communicator.say("Okay, lights turned on!")

    def action_scene(self, query):
        communicator = query.get_communicator()
        self.main_module.scene_relaxing()
        communicator.say('Ok, done!')

    key_regexes = {'(?i).*?(?=set)+.+?(?=light)+?(?=relaxing)+.': action_scene,
                   '((?i).*?(?=turn)+.+?(?=light)+.+?(?=on)+.)|'
                   '((?i).*?(?=turn)+.+?(?=on)+.+?(?=lights)+.)': action_on,
                   '((?i).*?(?=turn)+.+?(?=light)+.+?(?=off)+.)|'
                   '((?i).*?(?=turn)+.+?(?=off)+.+?(?=lights)+.)': action_off}
