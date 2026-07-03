class CommandBuilder:

    def __init__(self):
        pass

    def build(self, script, parameters):

        command = [

            "python3",

            script

        ]

        for key, value in parameters.items():

            if value is None:
                continue

            if value == "":
                continue

            command.append(f"--{key}")

            command.append(str(value))

        return " ".join(command)