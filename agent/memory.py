class Memory:

    def __init__(self, max_history=20):

        self.max_history = max_history
        self.messages = []

    def add_user(self, message):

        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )

        self._trim()

    def add_assistant(self, message):

        self.messages.append(
            {
                "role": "assistant",
                "content": message
            }
        )

        self._trim()

    def add_system(self, message):

        self.messages.append(
            {
                "role": "system",
                "content": message
            }
        )

        self._trim()

    def get(self):

        return self.messages

    def clear(self):

        self.messages = []

    def _trim(self):

        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]