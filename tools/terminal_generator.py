from ollama import chat

from config import MODEL


class TerminalGenerator:

    def __init__(self):

        self.prompt = """
You convert user requests into ONE terminal command.

Rules

Return ONLY the command.

No explanation.

No markdown.

No quotes.

Examples

Show files
dir

List folders
dir

Current directory
cd

IP address
ipconfig

Ping google
ping google.com
"""

    def generate(self, question):

        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": self.prompt
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        command = response["message"]["content"].strip()

        command = command.split("\n")[0]

        return command