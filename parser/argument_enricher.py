class ArgumentEnricher:

    RESOLVERS = {

        "station": "stations",
        "stations": "stations",

        "radio": "radios",
        "radios": "radios",

        "upstream": "ethernet",
        "upstream_port": "ethernet",

        "attenuator": "attenuators",

        "chamber": "chambers",

        "dut": "duts",

        "ssid": "ssids",

        "bssid": "bssids"
    }

    def enrich(self, arguments, required, multiple):

        required = set(required)
        multiple = set(multiple)

        enriched = []

        for arg in arguments:

            item = dict(arg)

            item["required"] = item["dest"] in required

            item["multiple"] = item["dest"] in multiple

            item["resolver"] = self.RESOLVERS.get(
                item["dest"],
                None
            )

            enriched.append(item)

        return enriched