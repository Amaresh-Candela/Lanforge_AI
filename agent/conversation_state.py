class ConversationState:

    def __init__(self):

        self.script = None

        self.parameters = {}

        self.execution = None

        self.waiting_for = None

    def reset(self):

        self.script = None

        self.parameters = {}

        self.execution = None

        self.waiting_for = None