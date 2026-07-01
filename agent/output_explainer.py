from ollama import chat
from config import MODEL


SYSTEM = """
You explain command output.

Be concise.

Use bullet points when appropriate.

If the command failed,
explain why.
"""


class OutputExplainer:

    def explain(self, question, command, output):

        prompt = f"""
User Question:

{question}

Executed Command:

{command}

Output:

{output}
"""

        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]