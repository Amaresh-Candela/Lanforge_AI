from agent.resource_ranker import ResourceRanker
class InventoryResolver:

    def __init__(self, inventory):

        self.inventory = inventory

        self.ranker = ResourceRanker()

    def resolve(self, required):

        resolved = {}

        missing = {}

        stations = self.ranker.rank_stations(
    self.inventory.get_stations()
)
        eth_ports = self.ranker.rank_eth_ports(
    self.inventory.get_eth_ports()
)
        radios = self.ranker.rank_radios(
    self.inventory.get_radios()
)

        for parameter in required:

            # ----------------------------
            # Station
            # ----------------------------

            if parameter in ["station", "stations"]:

                if len(stations) == 1:

                    resolved[parameter] = stations[0]

                elif len(stations) > 1:

                    missing[parameter] = stations

                else:

                    missing[parameter] = []

            # ----------------------------
            # Upstream
            # ----------------------------

            elif parameter in ["upstream", "upstream_port"]:

                if len(eth_ports) == 1:

                    resolved[parameter] = eth_ports[0]

                elif len(eth_ports) > 1:

                    missing[parameter] = eth_ports

                else:

                    missing[parameter] = []

            # ----------------------------
            # Radio
            # ----------------------------

            elif parameter == "radio":

                if len(radios) == 1:

                    resolved[parameter] = radios[0]

                elif len(radios) > 1:

                    missing[parameter] = radios

                else:

                    missing[parameter] = []

            else:

                missing[parameter] = []

        return {

            "resolved": resolved,

            "missing": missing

        }