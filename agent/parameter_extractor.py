import re


class ParameterExtractor:

    def extract(self, text):

        values = {}

        patterns = {

            "speed": r"(\d+\s*(?:kbps|mbps|gbps))",

            "duration": r"(\d+)\s*(?:sec|secs|second|seconds|min|mins|minute|minutes)"

        }

        for key, pattern in patterns.items():

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                values[key] = match.group(1)

        return values