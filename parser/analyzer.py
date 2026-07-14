import ast

from parser.argument_parser import ArgumentParser
from parser.import_parser import ImportParser
from parser.execution_analyzer import ExecutionAnalyzer


class ScriptAnalyzer:

    def __init__(self):

        self.argument_parser = ArgumentParser()

        self.import_parser = ImportParser()

        self.execution_analyzer = ExecutionAnalyzer()


    def analyze(self, filename):

        result = {}

        result["arguments"] = self.argument_parser.parse(filename)

        result["imports"] = self.import_parser.parse(filename)


        result["classes"] = self.get_classes(filename)

        result["functions"] = self.get_functions(filename)
        result["required"] = self.execution_analyzer.analyze(filename)

        return result

    def get_classes(self, filename):

        with open(filename, encoding="utf8", errors="ignore") as f:
            tree = ast.parse(f.read())

        classes = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                classes.append(node.name)

        return classes

    def get_functions(self, filename):

        with open(filename, encoding="utf8", errors="ignore") as f:
            tree = ast.parse(f.read())

        functions = []

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                functions.append(node.name)

        return functions