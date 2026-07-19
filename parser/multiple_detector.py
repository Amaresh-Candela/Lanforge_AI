import ast


class MultipleVisitor(ast.NodeVisitor):

    def __init__(self):

        self.multiple = set()

    def visit_Call(self, node):

        try:

            # Detect args.xxx.split(",")

            if isinstance(node.func, ast.Attribute):

                if node.func.attr == "split":

                    obj = node.func.value

                    if isinstance(obj, ast.Attribute):

                        if isinstance(obj.value, ast.Name):

                            if obj.value.id == "args":

                                self.multiple.add(obj.attr)

            # Detect argparse nargs

            if isinstance(node.func, ast.Attribute):

                if node.func.attr == "add_argument":

                    dest = None
                    multiple = False

                    for kw in node.keywords:

                        if kw.arg == "dest":

                            if isinstance(kw.value, ast.Constant):

                                dest = kw.value.value

                        elif kw.arg == "nargs":

                            if isinstance(kw.value, ast.Constant):

                                if kw.value.value in ["+", "*"]:

                                    multiple = True

                    if dest and multiple:

                        self.multiple.add(dest)

        except Exception:
            pass

        self.generic_visit(node)


class MultipleDetector:

    def analyze(self, filename):

        with open(
            filename,
            encoding="utf8",
            errors="ignore"
        ) as f:

            tree = ast.parse(f.read())

        visitor = MultipleVisitor()

        visitor.visit(tree)

        return sorted(visitor.multiple)