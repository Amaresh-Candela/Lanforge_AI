from agent.parameter_collector import ParameterCollector
from agent.command_builder import CommandBuilder
from agent.inventory_resolver import InventoryResolver
from tools.inventory import Inventory


class ExecutionPipeline:

    def __init__(self, host):

        self.inventory = Inventory(host)

        self.inventory_resolver = InventoryResolver(self.inventory)

        self.collector = ParameterCollector()

        self.builder = CommandBuilder()

    def prepare(
        self,
        script,
        execution,
        user_parameters=None
    ):

        if user_parameters is None:
            user_parameters = {}

        # Auto-fill from inventory
        inventory = self.inventory_resolver.resolve(
            execution["required"]
        )

        auto = inventory["resolved"]

        values = {}

        values.update(auto)

        values.update(user_parameters)

        result = self.collector.collect(
            execution,
            values
        )

        if not result["complete"]:

            return {

                "status": "missing",

                "missing": result["missing"],

                "known": result["values"]

            }

        command = self.builder.build(

            script,

            result["values"]

        )

        return {

            "status": "ready",

            "command": command

        }