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

                # if dest not supplied
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
                        "type": arg_type
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