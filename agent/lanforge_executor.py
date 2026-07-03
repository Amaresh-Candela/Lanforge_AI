import json

from agent.execution_pipeline import ExecutionPipeline
from agent.script_resolver import ScriptResolver


class LANforgeExecutor:

    def __init__(self, host):

        self.pipeline = ExecutionPipeline(host)

        self.script_resolver = ScriptResolver()

        with open(
            "knowledge/knowledge.json",
            encoding="utf8"
        ) as f:

            self.knowledge = json.load(f)

    def prepare(
        self,
        user_request,
        user_parameters=None
    ):

        if user_parameters is None:

            user_parameters = {}

        # -------------------------
        # Resolve Script
        # -------------------------

        result = self.script_resolver.resolve(
            user_request
        )

        script = result["script"]

        if script not in self.knowledge["scripts"]:

            return {

                "status": "error",

                "message": "Script not found."

            }

        info = self.knowledge["scripts"][script]

        execution = {

            "required": []

        }

        for arg in info["arguments"]:

            if arg.get("required"):

                execution["required"].append(
                    arg["dest"]
                )

        return self.pipeline.prepare(

            script,

            execution,

            user_parameters

        )