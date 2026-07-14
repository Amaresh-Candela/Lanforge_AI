class Conversation:

    def __init__(self):

        self.reset()

    def reset(self):
        self.stage = "required"

        self.optional_index = 0

        self.selected_optional = None

        self.use_optional = False

        self.active = False

        self.script = None

        self.arguments = []

        self.argument_info = {}

        self.index = 0

        self.values = {}

        self.optional = []

        self.ask_optional = False

    def start(self, script, required, optional, info):

        self.reset()

        self.active = True

        self.script = script

        self.arguments = required

        self.optional = optional

        self.argument_info = info

    def current(self):

        if self.index >= len(self.arguments):

            return None

        return self.arguments[self.index]

    def add(self, value):

        self.values[self.current()] = value

        self.index += 1

    def complete(self):

        return self.index >= len(self.arguments)