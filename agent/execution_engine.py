from agent.parameter_collector import ParameterCollector
from agent.command_builder import CommandBuilder


class ExecutionEngine:

    def __init__(self):

        self.collector = ParameterCollector()

        self.builder = CommandBuilder()

    def prepare(

        self,

        script,

        execution,

        parameters

    ):

        result = self.collector.collect(

            execution,

            parameters

        )

        if not result["complete"]:

            return {

                "status": "missing",

                "missing": result["missing"]

            }

        command = self.builder.build(

            script,

            result["values"]

        )

        return {

            "status": "ready",

            "command": command

        }