import json
import re

from ollama import chat
from config import MODEL


def ask_json(system_prompt, user_prompt):

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    text = response["message"]["content"]

    # Remove markdown fences
    text = text.replace("```json", "")
    text = text.replace("```", "")

    # Find first JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(f"No JSON found:\n{text}")

    return json.loads(match.group())