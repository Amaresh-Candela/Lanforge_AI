import json

from agent.execution_pipeline import ExecutionPipeline
from agent.script_resolver import ScriptResolver
from agent.runtime_manager import RuntimeManager
from agent.conversation import Conversation
from agent.conversation_manager import ConversationManager
from agent.resource_selector import ResourceSelector
from agent.parameter_planner import ParameterPlanner
from tools.ssh import SSHManager


class RuntimeInventoryAdapter:
    def __init__(self, runtime):
        self._runtime = runtime

    def __getattr__(self, name):
        return getattr(self._runtime, name)

    @property
    def connected(self):
        return self._runtime.connected

    @property
    def host(self):
        return self._runtime.host

    @property
    def raw(self):
        return self._runtime.raw

    @property
    def interfaces(self):
        return self._runtime.interfaces

    @property
    def stations(self):
        return self._runtime.stations

    @property
    def radios(self):
        return self._runtime.radios

    @property
    def ethernet(self):
        return self._runtime.ethernet

    @property
    def resources(self):
        return self._runtime.resources

    def get_stations(self):
        return sorted(self._runtime.stations.keys())

    def get_eth_ports(self):
        return sorted(self._runtime.ethernet.keys())

    def get_radios(self):
        return sorted(self._runtime.radios.keys())


class LANforgeExecutor:

    def __init__(self):

        self.runtime_manager = RuntimeManager()
        self.runtime = None
        self.runtime_view = None

        self.conversation = Conversation()
        self.conversation_manager = None

        self.script_resolver = ScriptResolver()
        self.selector = ResourceSelector()
        self.parameter_planner = ParameterPlanner()

        with open("knowledge/knowledge.json", encoding="utf8") as f:
            self.knowledge = json.load(f)

        self.pipeline = None
        self.ssh = None

    def connect(self, host):

        self.runtime = self.runtime_manager.connect(host)
        self.runtime_view = RuntimeInventoryAdapter(self.runtime)

        self.ssh = SSHManager(
            host=host,
            username="lanforge",
            password="lanforge"
        )
        self.ssh.connect()

        self.pipeline = ExecutionPipeline(self.runtime_view)
        self.conversation_manager = ConversationManager(self.runtime_view)

        return {
            "status": "connected",
            "host": host
        }

    def _build_execution(self, script):
        info = self.knowledge["scripts"][script]

        planner_required = self.parameter_planner.plan(script).get("required", [])
        required = planner_required or info.get("required", [])

        execution = {
            "required": required,
            "optional": [],
            "info": {}
        }

        required_set = set(required)

        for arg in info.get("arguments", []):
            dest = arg.get("dest")
            if not dest:
                continue

            execution["info"][dest] = arg

            if dest not in required_set:
                execution["optional"].append(dest)

        return execution

    def _execute_command(self, command):
        if self.ssh is None:
            return {
                "status": "error",
                "message": "SSH is not connected."
            }

        output = self.ssh.execute(command)

        return {
            "status": "completed",
            "stdout": output.get("stdout", ""),
            "stderr": output.get("stderr", "")
        }

    def _finalize_and_execute(self):
        execution = {
            "required": self.conversation.arguments,
            "optional": self.conversation.optional,
            "info": self.conversation.argument_info
        }

        result = self.pipeline.prepare(
            self.conversation.script,
            execution,
            self.conversation.values
        )

        self.conversation.reset()

        if result.get("status") == "ready":
            return self._execute_command(result["command"])

        return result

    def show_optional_parameters(self):
        if not self.conversation.optional:
            return (
                "No optional parameters are available.\n\n"
                "Type 'done' to execute."
            )

        text = "Available Optional Parameters\n\n"

        for i, parameter in enumerate(self.conversation.optional, start=1):
            info = self.conversation.argument_info.get(parameter, {})
            default = info.get("default", "")
            help_text = info.get("help", "")

            text += f"{i}. {parameter}\n"
            text += f"   Default: {default}\n"

            if help_text:
                text += f"   Help: {help_text}\n"

            text += "\n"

        text += "Type the parameter name to modify it, or type 'done' to execute."
        return text

    def ask(self, question):

        if self.runtime_view is None:
            return {
                "status": "connect",
                "message": "Please connect to a LANForge Manager first."
            }

        lower_question = question.strip().lower()

        if "connect" in lower_question and "lanforge" in lower_question:
            return {
                "status": "info",
                "message": "LANForge is already connected. Please enter a LANForge script request."
            }

        result = self.script_resolver.resolve(question)

        if not isinstance(result, dict):
            return {
                "status": "error",
                "message": "Script resolver returned an invalid result.",
                "details": str(result)
            }

        script = result.get("script", "")

        if not script:
            return {
                "status": "error",
                "message": result.get("reason", "I couldn't resolve a LANForge script.")
            }

        if script not in self.knowledge["scripts"]:
            return {
                "status": "error",
                "message": "I couldn't find a matching LANForge script."
            }

        execution = self._build_execution(script)

        pipeline_result = self.pipeline.prepare(
            script,
            execution,
            {}
        )

        if pipeline_result["status"] == "missing":

            missing = pipeline_result.get("missing", [])
            if not missing:
                return {
                    "status": "error",
                    "message": "Missing parameters could not be determined."
                }

            parameter = missing[0]

            self.conversation.start(
                script,
                execution["required"],
                execution["optional"],
                execution["info"]
            )
            self.conversation.stage = "required"
            self.conversation.selected_optional = None

            if self.conversation_manager is not None:
                return self.conversation_manager.ask(parameter)

            if parameter in ["station", "stations"]:
                resources = sorted(self.runtime_view.stations.keys())
                self.conversation.options = resources
                return self.selector.select_message("Stations", resources)

            elif parameter in ["upstream", "upstream_port"]:
                resources = sorted(self.runtime_view.ethernet.keys())
                self.conversation.options = resources
                return self.selector.select_message("Ethernet Ports", resources)

            elif parameter == "radio":
                resources = sorted(self.runtime_view.radios.keys())
                self.conversation.options = resources
                return self.selector.select_message("Radios", resources)

            info_item = execution["info"].get(parameter, {})
            message = f"Enter value for '{parameter}'."

            if info_item.get("help"):
                message += f"\n\nHelp: {info_item['help']}"

            return message

        if pipeline_result["status"] == "ready":
            return self._execute_command(pipeline_result["command"])

        return pipeline_result

    def continue_conversation(self, user_input):

        stage = getattr(self.conversation, "stage", "required")
        text = (user_input or "").strip()

        if stage == "optional_confirm":
            if text.lower() in ["y", "yes"]:
                self.conversation.stage = "optional_select"
                return self.show_optional_parameters()

            if text.lower() in ["n", "no", "done", "execute", "run", ""]:
                return self._finalize_and_execute()

            return "Please reply with y/n."

        if stage == "optional_select":
            if text.lower() in ["done", "execute", "run", "n", "no", ""]:
                return self._finalize_and_execute()

            if text not in self.conversation.optional:
                return self.show_optional_parameters()

            self.conversation.selected_optional = text
            self.conversation.stage = "optional_value"

            info = self.conversation.argument_info.get(text, {})
            default = info.get("default", "")
            help_text = info.get("help", "")

            message = f"Current default value: {default}\n\nEnter a new value or press Enter to keep the default."
            if help_text:
                message += f"\n\nHelp: {help_text}"

            return message

        if stage == "optional_value":
            parameter = getattr(self.conversation, "selected_optional", None)

            if not parameter:
                self.conversation.stage = "optional_select"
                return self.show_optional_parameters()

            info = self.conversation.argument_info.get(parameter, {})
            default = info.get("default", "")

            value = default if text == "" else text
            self.conversation.values[parameter] = value

            self.conversation.selected_optional = None
            self.conversation.stage = "optional_select"

            return self.show_optional_parameters()

        self.conversation.add(user_input)

        if not self.conversation.complete():
            next_parameter = self.conversation.current()
            return self.conversation_manager.ask(next_parameter)

        if self.conversation.optional:
            self.conversation.stage = "optional_confirm"
            return (
                "Required parameters collected.\n\n"
                "Would you like to configure optional parameters? (y/n)"
            )

        return self._finalize_and_execute()