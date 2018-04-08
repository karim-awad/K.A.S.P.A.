from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule


class AbstractBriefingSubmodule(AbstractSubmodule):
    """Abstract class for all plugin modules"""

    def briefing_action(self, query):
        """this method gets called as part of the briefing functionality of K.A.S.P.A.
            @param query mainly needed here to retrieve the communicator"""
        raise NotImplementedError()
        pass
