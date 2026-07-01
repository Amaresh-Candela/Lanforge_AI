from tools.terminal import run_terminal


class Executor:

    def execute(self, plan):

        tool = plan["tool"]

        if tool == "terminal":

            return run_terminal(
                plan["command"]
            )

        return None

    def convert(self, question):

        q = question.lower()

        if "current directory" in q:
            return "cd"

        if "files" in q:
            return "dir"

        if "directory" in q:
            return "dir"

        if "ip address" in q:
            return "ipconfig"

        if "hostname" in q:
            return "hostname"

        if "ping google" in q:
            return "ping google.com"

        if "who am i" in q:
            return "whoami"

        if "system info" in q:
            return "systeminfo"

        return q