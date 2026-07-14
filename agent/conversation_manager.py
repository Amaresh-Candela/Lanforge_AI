from agent.parameter_questions import QUESTIONS


class ConversationManager:

    def __init__(self, runtime):

        self.runtime = runtime

    def _build_option_list(self, title, options):

        if not options:
            return ""

        text = f"\n\nAvailable {title}:\n\n"

        for i, option in enumerate(options, start=1):
            text += f"{i}. {option}\n"

        text += (
            "\nYou can select:\n"
            "- A single number (e.g. 2)\n"
            "- Multiple numbers (e.g. 1,3,5)\n"
            "- 'all' to select everything\n"
        )

        return text

    def ask(self, parameter):

        message = QUESTIONS.get(
            parameter,
            f"Please provide '{parameter}'."
        )

        if parameter in ["station", "stations"]:

            stations = sorted(
                self.runtime.stations.keys()
            )

            message += self._build_option_list(
                "Stations",
                stations
            )

        elif parameter in ["upstream", "upstream_port"]:

            ports = sorted(
                self.runtime.ethernet.keys()
            )

            message += self._build_option_list(
                "Ethernet Ports",
                ports
            )

        elif parameter == "radio":

            radios = sorted(
                self.runtime.radios.keys()
            )

            message += self._build_option_list(
                "Radios",
                radios
            )

        return message