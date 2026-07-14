import json
from pathlib import Path

from ollama import chat

from config import MODEL


class AIMetadataBuilder:

    def __init__(self):

        with open(
            "knowledge/knowledge.json",
            encoding="utf8"
        ) as f:

            self.knowledge = json.load(f)

    def build(self):

        metadata = {}

        script_name = "lf_dataplane_test.py"

        if script_name not in self.knowledge["scripts"]:

            print(f"{script_name} not found.")

            return

        print(f"Analyzing {script_name}")

        info = self.knowledge["scripts"][script_name]

        metadata[script_name] = self.analyze_script(info)

        Path("knowledge").mkdir(exist_ok=True)

        with open(
            "knowledge/ai_metadata.json",
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4,
                ensure_ascii=False
            )

        print("\nAI metadata generated successfully.")

    def analyze_script(self, info):

        prompt = f"""
        You are a senior Candela Technologies LANForge automation engineer.

        Your task is to analyze ONE LANForge script and determine how an AI execution agent should run it.

        Script Name:
        {info["name"]}

        Arguments:
        {json.dumps(info["arguments"], indent=2)}

        Imports:
        {json.dumps(info["imports"], indent=2)}

        Classes:
        {json.dumps(info["classes"], indent=2)}

        Functions:
        {json.dumps(info["functions"], indent=2)}

        Your job is to infer:

        1. What the script does.
        2. Which arguments are REQUIRED before execution.
        3. Which arguments are OPTIONAL.
        4. Which arguments represent LANForge resources
        (station, radio, upstream, ethernet, attenuator, etc.).
        5. In what order the AI should ask the user for the required parameters.
        6. A realistic execution example.

        IMPORTANT:

        Do NOT simply copy the argparse "required" field.
        Many LANForge scripts use required=False even when an argument is mandatory.

        Infer the required parameters from:
        - argument names
        - help text
        - LANForge testing workflow
        - execution logic
        - engineering judgement

        Return ONLY valid JSON.

        Format:

        {{
            "purpose":"",
            "summary":"",
            "required":[],
            "optional":[],
            "resources": {{
                "station":"station",
                "upstream":"ethernet",
                "radio":"radio"
            }},
            "execution_order":[],
            "example":""
        }}

        No markdown.
        No explanation.
        Only JSON.
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

        try:

            return json.loads(text)

        except Exception:

            return {
                "purpose": "",
                "summary": "",
                "required": [],
                "optional": [],
                "resources": [],
                "execution_order": [],
                "example": "",
                "raw": text
            }