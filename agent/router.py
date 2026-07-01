import re


class Router:

    TERMINAL_PATTERNS = [

        # Execute commands
        r"\brun\b",
        r"\bexecute\b",
        r"\bopen\b",
        r"\bstart\b",
        r"\bstop\b",
        r"\bkill\b",
        r"\bclose\b",
        r"\brestart\b",

        # Networking
        r"\bip\b",
        r"\bipv4\b",
        r"\bipv6\b",
        r"\bipconfig\b",
        r"\bnetwork\b",
        r"\binternet\b",
        r"\bhostname\b",
        r"\bmac address\b",
        r"\bdns\b",
        r"\bgateway\b",
        r"\bping\b",
        r"\bnetstat\b",
        r"\bport\b",

        # Files
        r"\bdir\b",
        r"\bls\b",
        r"\bfile\b",
        r"\bfiles\b",
        r"\bfolder\b",
        r"\bdirectory\b",
        r"\bcurrent directory\b",

        # Processes
        r"\bprocess\b",
        r"\bprocesses\b",
        r"\btask\b",
        r"\btasklist\b",
        r"\bservice\b",

        # System
        r"\bsystem\b",
        r"\bwindows\b",
        r"\bcmd\b",
        r"\bcommand\b",
        r"\bpython version\b",
        r"\bpip\b",
        r"\bollama\b",

        # Browsers & Apps
        r"\bbrave\b",
        r"\bchrome\b",
        r"\bedge\b",
        r"\bfirefox\b",
        r"\bnotepad\b",

        # Identity
        r"\bwho am i\b",
        r"\busername\b",

    ]

    LANFORGE_PATTERNS = [

        r"lanforge",
        r"dataplane",
        r"wifi",
        r"station",
        r"attenuator",
        r"throughput",
        r"vap",
        r"cx",
        r"upstream",
        r"downstream",
        r"traffic"

    ]

    REPORT_PATTERNS = [

        r"report",
        r"csv",
        r"html",
        r"pdf",
        r"kpi"

    ]

    RAG_PATTERNS = [

        r"explain",
        r"documentation",
        r"parameter",
        r"readme",
        r"how does",
        r"what does"

    ]

    def route(self, question):

        q = question.lower().strip()

        for pattern in self.TERMINAL_PATTERNS:
            if re.search(pattern, q):
                return "terminal"

        for pattern in self.LANFORGE_PATTERNS:
            if re.search(pattern, q):
                return "lanforge"

        for pattern in self.REPORT_PATTERNS:
            if re.search(pattern, q):
                return "report"

        for pattern in self.RAG_PATTERNS:
            if re.search(pattern, q):
                return "rag"

        return "chat"