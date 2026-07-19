import ast
from pathlib import Path


class ArgumentVisitor(ast.NodeVisitor):

    def __init__(self):

        self.arguments = []

    def visit_Call(self, node):

        if isinstance(node.func, ast.Attribute):

            if node.func.attr == "add_argument":

                aliases = []
                dest = None
                default = None
                required = False
                help_text = ""
                arg_type = None

                choices = None
                nargs = None
                action = None
                metavar = None
                const = None

                # positional arguments
                for arg in node.args:

                    if isinstance(arg, ast.Constant):

                        aliases.append(arg.value)

                # keyword arguments
                for kw in node.keywords:

                    if kw.arg == "dest":

                        if isinstance(kw.value, ast.Constant):
                            dest = kw.value.value

                    elif kw.arg == "default":

                        if isinstance(kw.value, ast.Constant):
                            default = kw.value.value

                    elif kw.arg == "required":

                        if isinstance(kw.value, ast.Constant):
                            required = kw.value.value

                    elif kw.arg == "help":

                        if isinstance(kw.value, ast.Constant):
                            help_text = kw.value.value

                    elif kw.arg == "type":

                        if isinstance(kw.value, ast.Name):
                            arg_type = kw.value.id

                    elif kw.arg == "action":

                        if isinstance(kw.value, ast.Constant):
                            action = kw.value.value

                    elif kw.arg == "metavar":

                        if isinstance(kw.value, ast.Constant):
                            metavar = kw.value.value

                    elif kw.arg == "const":

                        if isinstance(kw.value, ast.Constant):
                            const = kw.value.value

                    elif kw.arg == "nargs":

                        if isinstance(kw.value, ast.Constant):
                            nargs = kw.value.value

                    elif kw.arg == "choices":

                        if isinstance(kw.value, ast.List):

                            choices = []

                            for item in kw.value.elts:

                                if isinstance(item, ast.Constant):

                                    choices.append(item.value)

                # infer dest if not supplied
                if dest is None:

                    for alias in aliases:

                        if alias.startswith("--"):

                            dest = alias.replace("--", "")
                            break

                self.arguments.append(

                    {

                        "dest": dest,

                        "aliases": aliases,

                        "default": default,

                        "required": required,

                        "help": help_text,

                        "type": arg_type,

                        "choices": choices,

                        "nargs": nargs,

                        "action": action,

                        "metavar": metavar,

                        "const": const

                    }

                )

        self.generic_visit(node)


class ArgumentParser:

    def parse(self, filename):

        filename = Path(filename)

        with open(
            filename,
            encoding="utf8",
            errors="ignore"
        ) as f:

            tree = ast.parse(f.read())

        visitor = ArgumentVisitor()

        visitor.visit(tree)

        return visitor.arguments