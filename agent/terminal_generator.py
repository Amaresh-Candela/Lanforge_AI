from ollama import chat
from config import MODEL


SYSTEM = """
You are a Windows CMD expert.

Your task is to convert the user's request into ONE Windows CMD command.

Rules:

1. Return ONLY the command.
2. No explanation.
3. No markdown.
4. No quotes.
5. No code block.
6. Never answer the user's question directly.

Examples

User:
What is my IP?
Command:
ipconfig

User:
Show my IPv4
Command:
ipconfig

User:
Display network configuration
Command:
ipconfig

User:
Show hostname
Command:
hostname

User:
Who am I?
Command:
whoami

User:
Show current directory
Command:
cd

User:
List files
Command:
dir

User:
Stop Brave browser
Command:
taskkill /IM brave.exe /F

User:
Show running processes
Command:
tasklist

User:
Show listening ports
Command:
netstat -ano

Return ONLY the command.
"""


class TerminalGenerator:

    def generate(self, question):

        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return response["message"]["content"].strip()
