class Planner:

    def plan(self, question: str):

        q = question.lower().strip()

        # ------------------------
        # Greetings
        # ------------------------

        greetings = [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]

        if q in greetings:
            return {
                "tool": "chat"
            }

        # ------------------------
        # Terminal Requests
        # ------------------------

        terminal_keywords = {

            "ip": "ipconfig",
            "ip address": "ipconfig",
            "network": "ipconfig",

            "hostname": "hostname",

            "who am i": "whoami",
            "username": "whoami",

            "current directory": "cd",
            "pwd": "cd",

            "files": "dir",
            "folder": "dir",
            "directory": "dir",

            "processes": "tasklist",

            "system information": "systeminfo",

            "date": "date",

            "time": "time",

            "python version": "python --version",

            "ollama models": "ollama list",

            "ping google": "ping google.com"

        }

        for key, command in terminal_keywords.items():

            if key in q:

                return {
                    "tool": "terminal",
                    "command": command
                }

        # ------------------------
        # LANforge
        # ------------------------

        lanforge_words = [
            "lanforge",
            "dataplane",
            "wifi",
            "station",
            "attenuator",
            "throughput"
        ]

        if any(word in q for word in lanforge_words):

            return {
                "tool": "lanforge",
                "question": question
            }

        # ------------------------
        # Documentation
        # ------------------------

        docs = [
            "explain",
            "documentation",
            "readme",
            "parameter"
        ]

        if any(word in q for word in docs):

            return {
                "tool": "rag",
                "query": question
            }

        return {
            "tool": "chat"
        }