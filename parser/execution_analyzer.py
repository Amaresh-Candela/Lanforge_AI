import ast


class RequiredArgumentVisitor(ast.NodeVisitor):

    def __init__(self):

        self.required = set()

    def visit_If(self, node):

        self.check(node.test)

        self.generic_visit(node)

    def visit_Call(self, node):

        # parser.error("...")
        if isinstance(node.func, ast.Attribute):

            if node.func.attr == "error":

                for arg in ast.walk(node):

                    if isinstance(arg, ast.Attribute):

                        if isinstance(arg.value, ast.Name):

                            if arg.value.id == "args":

                                self.required.add(arg.attr)

        self.generic_visit(node)

    def check(self, node):

        # if not args.station
        if isinstance(node, ast.UnaryOp):

            if isinstance(node.op, ast.Not):

                operand = node.operand

                if isinstance(operand, ast.Attribute):

                    if isinstance(operand.value, ast.Name):

                        if operand.value.id == "args":

                            self.required.add(
                                operand.attr
                            )

        # if args.station == ""
        elif isinstance(node, ast.Compare):

            left = node.left

            if isinstance(left, ast.Attribute):

                if isinstance(left.value, ast.Name):

                    if left.value.id == "args":

                        self.required.add(
                            left.attr
                        )

        # len(args.station)
        elif isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id == "len":

                    for arg in node.args:

                        if isinstance(arg, ast.Attribute):

                            if isinstance(arg.value, ast.Name):

                                if arg.value.id == "args":

                                    self.required.add(
                                        arg.attr
                                    )


class ExecutionAnalyzer:

    def analyze(self, filename):

        with open(

            filename,

            encoding="utf8",

            errors="ignore"

        ) as f:

            tree = ast.parse(f.read())

        visitor = RequiredArgumentVisitor()

        visitor.visit(tree)

        return sorted(visitor.required)