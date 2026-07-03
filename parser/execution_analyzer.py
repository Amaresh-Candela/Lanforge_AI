class ExecutionAnalyzer:

    def __init__(self):
        pass

    def analyze(self, script_name, arguments):

        execution = {

            "script": script_name,

            "required": [],

            "optional": [],

            "aliases": {},

            "defaults": {},

            "help": {}

        }

        for arg in arguments:

            dest = arg.get("dest")

            aliases = arg.get("aliases", [])

            default = arg.get("default")

            help_text = arg.get("help", "")

            required = arg.get("required", False)

            if required:
                execution["required"].append(dest)
            else:
                execution["optional"].append(dest)

            execution["aliases"][dest] = aliases

            execution["defaults"][dest] = default

            execution["help"][dest] = help_text

        return execution