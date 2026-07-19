class MetadataEnricher:

    RESOURCE_RESOLVERS = {

        "station": "stations",
        "stations": "stations",

        "radio": "radios",
        "radios": "radios",

        "upstream": "ethernet",
        "upstream_port": "ethernet",

        "attenuator": "attenuators",
        "attenuators": "attenuators",

        "chamber": "chambers",

        "dut": "duts",

        "ssid": "ssids",
        "bssid": "bssids"
    }

    TYPE_MAP = {

        "str": "string",
        "int": "integer",
        "float": "float",
        "bool": "boolean"
    }

    def enrich(self, script):

        script = dict(script)

        script["arguments"] = self.enrich_arguments(
            script.get("arguments", []),
            script.get("required", [])
        )

        return script

    def enrich_arguments(self, arguments, required):

        enriched = []

        required = set(required)

        for arg in arguments:

            item = dict(arg)

            item["required"] = (
                item.get("dest") in required
            )

            item["multiple"] = False

            item["resolver"] = self.detect_resolver(
                item.get("dest", "")
            )

            item["choices"] = item.get(
                "choices",
                None
            )

            item["value_type"] = self.detect_type(
                item.get("type")
            )

            enriched.append(item)

        return enriched

    def detect_resolver(self, dest):

        return self.RESOURCE_RESOLVERS.get(
            dest.lower(),
            None
        )

    def detect_type(self, value):

        if value is None:
            return "string"

        if isinstance(value, str):
            return self.TYPE_MAP.get(
                value,
                value
            )

        name = getattr(
            value,
            "__name__",
            "string"
        )

        return self.TYPE_MAP.get(
            name,
            "string"
        )