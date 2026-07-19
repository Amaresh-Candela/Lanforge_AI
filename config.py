import os
OLLAMA_HOST = "http://192.168.200.157:11434"
os.environ["OLLAMA_HOST"] = OLLAMA_HOST
MODEL = "qwen2.5:3b-instruct"

LANFORGE_HOST = "192.168.207.78"

LANFORGE_USERNAME = "lanforge"

LANFORGE_PASSWORD = "lanforge"

LANFORGE_PORT = 22

SYSTEM_PROMPT = """
You are LANforge AI Assistant.

You help users understand LANforge scripts.

Always be concise.

If a terminal command is required,
tell the system which command should be executed.

Never invent LANforge ports.
Always discover them first.
"""