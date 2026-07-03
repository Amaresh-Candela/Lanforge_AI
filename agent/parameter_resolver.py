from ollama import chat

from config import MODEL
from rag.retriever import Retriever


class ParameterResolver:

    def __init__(self):

        self.rag = Retriever()

    def resolve(self, script):

        docs = self.rag.search(script, top_k=5)

        context = ""

        for doc in docs:

            context += f"""

FILE:
{doc['file']}

CONTENT:
{doc['text']}

"""

        prompt = f"""
You are a LANforge expert.

Your task is to determine the parameters required to execute the given LANforge script.

Use ONLY the documentation below.

Return ONLY valid JSON.

Example:

{{
    "script":"lf_dataplane_test.py",
    "required":[
        "station",
        "upstream_port",
        "rate"
    ],
    "optional":[
        "duration",
        "report",
        "debug"
    ]
}}

If no information is available:

{{
    "script":"{script}",
    "required":[],
    "optional":[]
}}

Documentation:

{context}

Target Script:

{script}
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

        return response["message"]["content"]