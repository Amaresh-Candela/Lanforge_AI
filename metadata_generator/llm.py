import json
from ollama import Client

from .prompt import SYSTEM_PROMPT

HOST = "http://192.168.200.157:11434"
MODEL = "gpt-oss:20b"

client = Client(host=HOST)


def analyze(script_source: str, parser_metadata: dict) -> dict:
    user_prompt = f"""
==========================
PYTHON SCRIPT
==========================

{script_source}

==========================
PARSER METADATA
==========================

{json.dumps(parser_metadata, indent=2)}

==========================

Generate the semantic metadata.
Return ONLY valid JSON.
"""

    response = client.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    print("=" * 80)
    print("FULL RESPONSE")
    print("=" * 80)
    print(response)
    print("=" * 80)

    message = response.get("message", {})
    text = message.get("content", "")

    print("Content length:", len(text))
    print("First 500 chars:")
    print(repr(text[:500]))

    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        text = "\n".join(lines)

    try:
        return json.loads(text)
    except Exception as e:
        print("\nJSON PARSE FAILED")
        print(e)

        with open("llm_response.txt", "w", encoding="utf-8") as f:
            f.write(text)

        print("Saved raw response to llm_response.txt")
        raise