import ast


class ImportVisitor(ast.NodeVisitor):

    def __init__(self):

        self.imports = []

    def visit_Import(self, node):

        for module in node.names:

            self.imports.append(module.name)

    def visit_ImportFrom(self, node):

        if node.module:

            self.imports.append(node.module)

        self.generic_visit(node)


class ImportParser:

    def parse(self, filename):

        with open(
            filename,
            encoding="utf8",
            errors="ignore"
        ) as f:

            tree = ast.parse(f.read())

        visitor = ImportVisitor()

        visitor.visit(tree)

        return sorted(list(set(visitor.imports)))