import json

from ollama import chat

from config import MODEL

from knowledge.context_builder import ContextBuilder


class ParameterPlanner:

    def __init__(self):

        self.context = ContextBuilder()

    def plan(self, script):

        context = self.context.build(script)

        prompt = f"""
You are a LANForge engineer.

Below is the complete source code and metadata of a LANForge script.

Determine ONLY the parameters that a user must provide before this script can be executed.

Do NOT include optional arguments.

Do NOT include debugging arguments.

Do NOT include logging arguments.

Do NOT include json configuration arguments.

Return ONLY valid JSON.

Example:

{{
    "required":[
        "station",
        "upstream",
        "speed"
    ]
}}

Context

{context}
"""

        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        text = response["message"]["content"]

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        try:

            return json.loads(text)

        except Exception:

            return {

                "required": []

            }