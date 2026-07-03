class ParameterCollector:

    def __init__(self):

        self.values = {}

    def collect(self, execution, user_values=None):

        if user_values is None:
            user_values = {}

        missing = []

        required = execution.get("required", [])

        for parameter in required:

            if parameter in user_values:

                self.values[parameter] = user_values[parameter]

            else:

                missing.append(parameter)

        return {

            "complete": len(missing) == 0,

            "missing": missing,

            "values": self.values

        }