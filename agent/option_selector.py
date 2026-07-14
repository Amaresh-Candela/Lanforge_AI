class OptionSelector:

    def select(self, user_input, options):

        if not options:
            return []

        text = user_input.strip().lower()

        if text == "all":
            return options

        result = []

        parts = text.split(",")

        for part in parts:

            part = part.strip()

            if part.isdigit():

                index = int(part) - 1

                if 0 <= index < len(options):

                    result.append(options[index])

            else:

                if part in options:

                    result.append(part)

        return result