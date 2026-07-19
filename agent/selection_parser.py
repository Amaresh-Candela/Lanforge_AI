class SelectionParser:

    def parse(self, text, options, multiple):

        text = text.strip().lower()

        if multiple and text == "all":
            return options

        parts = [x.strip() for x in text.split(",")]

        values = []

        for part in parts:

            if part.isdigit():

                index = int(part) - 1

                if 0 <= index < len(options):

                    values.append(options[index])

            else:

                values.append(part)

        if multiple:
            return values

        return values[0] if values else ""
