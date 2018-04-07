from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.core_modules.conversation_module.conversationModuleEn import ConversationModuleEn
from Kaspa.modules.core_modules.conversation_module.conversationModuleDe import ConversationModuleDe


class ConversationModuleMain(AbstractModule):

    module_name = "Conversation"

    def __init__(self):
        super(ConversationModuleMain, self).__init__()
        # Found no use for a german module at the moment
        self.add_submodule(ConversationModuleEn())
        self.add_submodule(ConversationModuleDe())
