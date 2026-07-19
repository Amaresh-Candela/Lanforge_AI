from agent.parameter_questions import QUESTIONS


class ConversationManager:

    def __init__(self, runtime):

        self.runtime = runtime

    def _build_option_list(self, title, options, multiple):

        if not options:
            return ""

        text = f"\n\nAvailable {title}:\n\n"

        for i, option in enumerate(options, start=1):

            text += f"{i}. {option}\n"

        text += "\nYou can select:\n"

        if multiple:

            text += (
                "- A single number (e.g. 2)\n"
                "- Multiple numbers (e.g. 1,3,5)\n"
                "- all\n"
            )

        else:

            text += "- A single number (e.g. 2)\n"

        return text

    def ask(self, argument):

        parameter = argument["dest"]

        message = QUESTIONS.get(

            parameter,

            f"Please provide '{parameter}'."

        )

        resolver = argument.get("resolver")

        multiple = argument.get("multiple", False)

        if resolver:

            options = sorted(

                getattr(

                    self.runtime,

                    resolver,

                    {}

                ).keys()

            )
            self.runtime.current_options = options

            title = resolver.replace("_", " ").title()

            message += self._build_option_list(

                title,

                options,

                multiple

            )

        elif argument.get("choices"):

            choices = argument["choices"]

            message += self._build_option_list(

                "Choices",

                choices,

                multiple

            )

        elif argument.get("default") not in [None, ""]:

            message += (

                f"\n\nDefault Value : "

                f"{argument['default']}"

            )

        return message