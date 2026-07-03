class ResourceRanker:

    def __init__(self):
        pass

    def rank_eth_ports(self, ports):

        score = []

        for port in ports:

            s = 0

            if ".eth" in port:
                s += 100

            if port.startswith("1.1"):
                s += 50

            if "rmnet" in port:
                s -= 100

            if "umts" in port:
                s -= 100

            score.append(
                (s, port)
            )

        score.sort(reverse=True)

        return [p for _, p in score]

    def rank_radios(self, radios):

        score = []

        for radio in radios:

            s = 0

            if radio.startswith("1.1"):
                s += 100

            if "wiphy" in radio:
                s += 50

            score.append(
                (s, radio)
            )

        score.sort(reverse=True)

        return [p for _, p in score]

    def rank_stations(self, stations):

        score = []

        for sta in stations:

            s = 0

            if sta.startswith("1.1"):
                s += 100

            score.append(
                (s, sta)
            )

        score.sort(reverse=True)

        return [p for _, p in score]