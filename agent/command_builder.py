class CommandBuilder:

    def __init__(self):

        self.script_root = "/home/lanforge/scripts/py-scripts"

    def build(self, script, parameters):

        command = [

            "cd",

            self.script_root,

            "&&",

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