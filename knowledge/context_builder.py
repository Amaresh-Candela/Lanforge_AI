import json
from pathlib import Path


class ContextBuilder:

    def __init__(self):

        with open(
            "knowledge/knowledge.json",
            encoding="utf8"
        ) as f:

            self.knowledge = json.load(f)

    def build(self, script_name):

        if script_name not in self.knowledge["scripts"]:

            return None

        info = self.knowledge["scripts"][script_name]

        source = ""

        try:

            source = Path(
                info["path"]
            ).read_text(
                encoding="utf8",
                errors="ignore"
            )

        except Exception:
            pass

        return {

            "script": info,

            "source": source

        }