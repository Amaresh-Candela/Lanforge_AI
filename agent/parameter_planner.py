import json

from ollama import chat

from config import MODEL

from knowledge.context_builder import ContextBuilder


class ParameterPlanner:

    def __init__(self):

        self.context = ContextBuilder()

    def plan(self, script):

        context_dict = self.context.build(script)
        if context_dict:
            context_dict["source"] = "Omitted for context size limit"
        context = json.dumps(context_dict, indent=4)

        prompt = f"""
You are a LANForge engineer.

Below is the metadata of a LANForge script.

Determine ONLY the parameters that a user must provide before this script can be executed successfully.

Important Rules:
1. Always include 'dut' (if present in the script's arguments) as a required parameter for any WiFi, station, or dataplane test scripts, as these tests cannot run without a target Device Under Test.
2. Always include 'local_lf_report_dir' (if present in the arguments) as a required parameter to ensure reports can be successfully pulled.
3. Do NOT include optional debugging, logging, or help flags.

Return ONLY valid JSON.

Example:

{{
    "required":[
        "station",
        "upstream",
        "speed",
        "dut",
        "local_lf_report_dir"
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