import requests

from agent.runtime import LANForgeRuntime


class RuntimeManager:

    def __init__(self):

        self.runtime = LANForgeRuntime()

    def connect(self, host):

        url = f"http://{host}:8080/ports/all"

        r = requests.get(url, timeout=10)

        r.raise_for_status()

        data = r.json()

        self.runtime.reset()

        self.runtime.connected = True

        self.runtime.host = host

        self.runtime.raw = data

        interfaces = data.get("interfaces", [])

        for item in interfaces:

            for eid, info in item.items():

                self.runtime.interfaces[eid] = info

                port_type = info.get("port type", "")

                if port_type == "Ethernet":

                    self.runtime.ethernet[eid] = info

                elif port_type == "WIFI-STA":

                    self.runtime.stations[eid] = info

                elif port_type == "WIFI-Radio":

                    self.runtime.radios[eid] = info

        return self.runtime