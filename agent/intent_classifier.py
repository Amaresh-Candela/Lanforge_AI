from ollama import chat
from config import MODEL


class IntentClassifier:

    def __init__(self):

        self.system_prompt = """
You are an intent classifier.

Classify the user's request into EXACTLY ONE of these intents.

chat
terminal
lanforge
rag
report
inventory

Return ONLY one word.

No punctuation.

No explanation.
"""

        self.rag_keywords = [
            "what is",
            "explain",
            "meaning",
            "define",
            "documentation",
            "parameter",
            "argument",
            "arguments",
            "alias",
            "aliases",
            "script",
            "compare",
            "difference",
            "lf_",
            "traffic_port",
            "upstream",
            "station",
            "radio",
            "ssid",
            "security",
            "password",
            "dataplane",
            "wifi capacity"
        ]

        self.lanforge_keywords = [
            "run dataplane",
            "run wifi",
            "wifi capacity",
            "run ftp",
            "ftp test",
            "create l3",
            "create station",
            "run roaming",
            "run script",
            "execute script",
            "start test"
        ]

        self.terminal_keywords = [
            "run ",
            "execute ",
            "cmd",
            "terminal",
            "powershell",
            "ipconfig",
            "dir",
            "ls",
            "mkdir",
            "ping",
            "netstat",
            "tasklist",
            "whoami"
        ]

        self.report_keywords = [
            "report",
            "summary",
            "summarize",
            "kpi",
            "latency",
            "throughput",
            "packet loss",
            "download report"
        ]

        self.inventory_keywords = [
            "show stations",
            "list stations",
            "available stations",
            "show radios",
            "show attenuators",
            "show ports",
            "inventory",
            "resources"
        ]

    def classify(self, question):

        q = question.lower()

        # ---------- LANforge Execution ----------

        if any(x in q for x in self.lanforge_keywords):
            return "lanforge"

        # ---------- RAG ----------

        if any(x in q for x in self.rag_keywords):
            return "rag"

        # ---------- Terminal ----------

        if any(x in q for x in self.terminal_keywords):
            return "terminal"

        # ---------- Reports ----------

        if any(x in q for x in self.report_keywords):
            return "report"

        # ---------- Inventory ----------

        if any(x in q for x in self.inventory_keywords):
            return "inventory"

        # ---------- LLM Fallback ----------

        response = chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        intent = response["message"]["content"].strip().lower()

        valid = {
            "chat",
            "terminal",
            "lanforge",
            "rag",
            "report",
            "inventory"
        }

        if intent not in valid:
            return "chat"

        return intent