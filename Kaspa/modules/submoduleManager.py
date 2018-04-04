class SubmoduleManager(object):
    submodules = dict()

    def get_submodule(self, language):
        return self.submodules[language]

    def add_submodule(self, submodule):
        self.submodules[submodule.get_language()] = submodule

    def remove_submodule(self, submodule):
        self.submodules.pop(submodule.get_language())
