import json

from agent.selection_parser import SelectionParser
from agent.execution_pipeline import ExecutionPipeline
from agent.script_resolver import ScriptResolver
from agent.runtime_manager import RuntimeManager
from agent.conversation import Conversation
from agent.conversation_manager import ConversationManager
from agent.resource_selector import ResourceSelector
from agent.parameter_planner import ParameterPlanner
from agent.entity_extractor import EntityExtractor
from tools.ssh import SSHManager
from agent.parameter_extractor import ParameterExtractor


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
        from agent.entity_extractor import EntityExtractor
        self.entity_extractor = EntityExtractor()
        self.runtime_manager = RuntimeManager()
        self.runtime = None
        self.runtime_view = None

        self.conversation = Conversation()
        self.conversation_manager = None

        self.script_resolver = ScriptResolver()
        self.selector = ResourceSelector()
        self.parameter_planner = ParameterPlanner()
        self.parameter_extractor = ParameterExtractor()
        self.selection_parser = SelectionParser()

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

        from agent.script_overrides import SCRIPT_OVERRIDES
        override = SCRIPT_OVERRIDES.get(script)

        if override:
            required = list(override["required"])
            optional = list(override["optional"])
            
            execution = {
                "required": required,
                "optional": optional,
                "info": {}
            }
            required_set = set(required)
            optional_set = set(optional)
            
            for arg in info.get("arguments", []):
                dest = arg.get("dest")
                if dest in required_set or dest in optional_set:
                    arg_copy = dict(arg)
                    if dest == "traffic_types":
                        arg_copy["choices"] = ["UDP", "TCP"]
                    elif dest == "traffic_directions":
                        arg_copy["choices"] = ["DUT-TX", "DUT-RX"]
                    elif dest == "spatial_streams":
                        arg_copy["choices"] = ["1", "2", "3", "4", "AUTO"]
                    elif dest == "bandwidths":
                        arg_copy["choices"] = ["20", "40", "80", "160", "320"]
                    elif dest == "channels":
                        arg_copy["choices"] = ["6", "11", "36", "40", "44", "48", "149", "153", "157", "161"]
                    execution["info"][dest] = arg_copy
            return execution

        planner_required = self.parameter_planner.plan(script).get("required", [])
        info_required = [arg["dest"] for arg in info.get("arguments", []) if arg.get("required")]
        required = planner_required or info_required

        # Dynamic safety net for wireless and report settings
        all_dests = {arg["dest"] for arg in info.get("arguments", []) if arg.get("dest")}
        if "dut" in all_dests and ("wifi" in script or "dataplane" in script or "roam" in script or "rvr" in script):
            if "dut" not in required:
                required.append("dut")
        if "local_lf_report_dir" in all_dests:
            if "local_lf_report_dir" not in required:
                required.append("local_lf_report_dir")

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
        values = self.parameter_extractor.extract(question)

        result = self.script_resolver.resolve(question)

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
            values
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
            # Pre-populate already extracted/auto-resolved values
            known_values = {}
            known_values.update(pipeline_result.get("known", {}))
            known_values.update(values)
            for k, v in known_values.items():
                if k in execution["required"] or k in execution["optional"]:
                    self.conversation.values[k] = v

            argument = execution["info"][parameter]

            resolver = argument.get("resolver")

            if resolver:

                self.conversation.options = sorted(

                    getattr(

                        self.runtime_view,

                        resolver,

                        {}

                    ).keys()

                )

            else:

                self.conversation.options = []

            return self.conversation_manager.ask(argument)

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

            resolver = info.get("resolver")
            choices = info.get("choices")

            if resolver:
                options = sorted(
                    getattr(
                        self.runtime_view,
                        resolver,
                        {}
                    ).keys()
                )
                self.conversation.options = options
                title = resolver.replace("_", " ").title()
                message += f"\n\nAvailable {title}:\n\n"
                for i, opt in enumerate(options, start=1):
                    message += f"{i}. {opt}\n"
                message += "\nYou can select by number or list (if multiple)."
            elif choices:
                self.conversation.options = choices
                message += f"\n\nAvailable Choices:\n\n"
                for i, opt in enumerate(choices, start=1):
                    message += f"{i}. {opt}\n"
                message += "\nYou can select by number or list (if multiple)."
            else:
                self.conversation.options = []

            return message

        if stage == "optional_value":
            parameter = getattr(self.conversation, "selected_optional", None)

            if not parameter:
                self.conversation.stage = "optional_select"
                return self.show_optional_parameters()

            info = self.conversation.argument_info.get(parameter, {})
            default = info.get("default", "")
            multiple = info.get("multiple", False)

            if text == "":
                value = default
            elif self.conversation.options:
                resolved_value = self.selection_parser.parse(text, self.conversation.options, multiple)
                if isinstance(resolved_value, list):
                    value = ",".join(resolved_value)
                else:
                    value = resolved_value
            else:
                value = text

            self.conversation.values[parameter] = value

            self.conversation.selected_optional = None
            self.conversation.stage = "optional_select"
            self.conversation.options = []

            return self.show_optional_parameters()

        current_param = self.conversation.current()
        arg_info = self.conversation.argument_info.get(current_param, {})
        multiple = arg_info.get("multiple", False)

        if self.conversation.options:
            resolved_value = self.selection_parser.parse(user_input, self.conversation.options, multiple)
            # If resolved_value is a list, format it as a comma-separated string for command-line compatibility
            if isinstance(resolved_value, list):
                resolved_value = ",".join(resolved_value)
        else:
            resolved_value = user_input

        self.conversation.add(resolved_value)

        if not self.conversation.complete():
            next_parameter = self.conversation.current()
            argument_dict = self.conversation.argument_info.get(next_parameter, {})
            return self.conversation_manager.ask(argument_dict)

        if self.conversation.optional:
            self.conversation.stage = "optional_confirm"
            return (
                "Required parameters collected.\n\n"
                "Would you like to configure optional parameters? (y/n)"
            )

        return self._finalize_and_execute()