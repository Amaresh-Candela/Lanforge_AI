import re


class EntityExtractor:

    def extract(self, text):

        entities = {}

        # LANForge IP
        ip = re.search(
            r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            text
        )

        if ip:

            entities["host"] = ip.group()

        # duration
        duration = re.search(
            r"(\d+)\s*(sec|secs|second|seconds|min|mins|minute|minutes)",
            text,
            re.IGNORECASE
        )

        if duration:

            entities["duration"] = duration.group(1)

        # speed
        speed = re.search(
            r"\d+\s*(kbps|mbps|gbps)",
            text,
            re.IGNORECASE
        )

        if speed:

            entities["speed"] = speed.group()

        return entities