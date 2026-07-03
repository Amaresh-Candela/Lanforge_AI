import ast


class RequirementVisitor(ast.NodeVisitor):

    def __init__(self):

        self.required = set()

    def visit_If(self, node):

        try:

            test = node.test

            # if args.station == ""
            if isinstance(test, ast.Compare):

                left = test.left

                if isinstance(left, ast.Attribute):

                    if isinstance(left.value, ast.Name):

                        if left.value.id == "args":

                            self.required.add(left.attr)

            # if not args.station
            elif isinstance(test, ast.UnaryOp):

                if isinstance(test.op, ast.Not):

                    operand = test.operand

                    if isinstance(operand, ast.Attribute):

                        if isinstance(operand.value, ast.Name):

                            if operand.value.id == "args":

                                self.required.add(
                                    operand.attr
                                )

        except Exception:
            pass

        self.generic_visit(node)


class RequirementInference:

    def infer(self, filename):

        with open(
            filename,
            encoding="utf8",
            errors="ignore"
        ) as f:

            tree = ast.parse(f.read())

        visitor = RequirementVisitor()

        visitor.visit(tree)

        return sorted(list(visitor.required))