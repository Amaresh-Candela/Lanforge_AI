import requests


class Inventory:

    def __init__(self, host, port=8080):

        self.base = f"http://{host}:{port}"

    def _interfaces(self):

        r = requests.get(
            f"{self.base}/ports/all",
            timeout=10
        )

        data = r.json()

        return data.get("interfaces", [])

    def get_stations(self):

        stations = []

        for item in self._interfaces():

            for eid, info in item.items():

                alias = info.get("alias", "")

                if "sta" in alias.lower():

                    stations.append(eid)

        return sorted(stations)

    def get_eth_ports(self):

        ports = []

        for item in self._interfaces():

            for eid, info in item.items():

                if info.get("port type") == "Ethernet":

                    ports.append(eid)

        return sorted(ports)

    def get_radios(self):

        radios = []

        for item in self._interfaces():

            for eid, info in item.items():

                device = info.get("device", "")

                if "wiphy" in device.lower():

                    radios.append(eid)

        return sorted(radios)

    def get_all_ports(self):

        ports = []

        for item in self._interfaces():

            for eid, info in item.items():

                ports.append({

                    "eid": eid,

                    "alias": info.get("alias", ""),

                    "device": info.get("device", ""),

                    "type": info.get("port type", ""),

                    "ip": info.get("ip", ""),

                    "mac": info.get("mac", "")

                })

        return ports