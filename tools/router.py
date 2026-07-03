from tools.terminal import run_terminal


class Router:

    def __init__(self):

        pass

    def execute(self, plan):

        tool = plan["tool"]

        if tool == "terminal":

            return self.run_terminal(plan)

        elif tool == "lanforge":

            return self.run_lanforge(plan)

        elif tool == "rag":

            return self.run_rag(plan)

        elif tool == "inventory":

            return self.run_inventory(plan)

        elif tool == "report":

            return self.run_report(plan)

        return None

    def run_terminal(self, plan):

        result = run_terminal(plan["command"])

        output = result["stdout"]

        if output.strip() == "":
            output = result["stderr"]

        return output

    def run_lanforge(self, plan):

        return "LANforge module not implemented."

    def run_rag(self, plan):

        return "RAG module not implemented."

    def run_inventory(self, plan):

        return "Inventory module not implemented."

    def run_report(self, plan):

        return "Report module not implemented."