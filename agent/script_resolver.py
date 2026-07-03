import json

from ollama import chat

from config import MODEL
from rag.retriever import Retriever


class ScriptResolver:

    def __init__(self):

        self.rag = Retriever()

    def resolve(self, question):

        docs = self.rag.search(question, top_k=3)

        context = ""

        for doc in docs:

            if doc["folder"] not in ["commands", "scripts"]:
                continue

            context += f"""

FILE:
{doc['file']}

CONTENT:
{doc['text']}

"""

        prompt = f"""
You are a LANforge script resolver.

Determine which LANforge Python script should be executed.

Return ONLY valid JSON.

Example:

{{
    "script":"lf_dataplane_test.py",
    "confidence":0.98,
    "reason":"Matched dataplane documentation."
}}

If nothing matches return

{{
    "script":"",
    "confidence":0.0,
    "reason":"No matching script found."
}}

Documentation

{context}

User Request

{question}
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

        text = response["message"]["content"].strip()

        # Remove markdown fences if the model adds them
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        try:

            return json.loads(text)

        except Exception:

            return {

                "script": "",

                "confidence": 0.0,

                "reason": text

            }