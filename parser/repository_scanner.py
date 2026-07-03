from pathlib import Path


class RepositoryScanner:

    def __init__(self, root):

        self.root = Path(root)

    def scan(self):

        scripts = []

        for file in self.root.rglob("*.py"):

            scripts.append(file)

        return sorted(scripts)

    def scan_py_scripts(self):

        scripts = []

        py_scripts = self.root / "py-scripts"

        if py_scripts.exists():

            for file in py_scripts.rglob("*.py"):

                scripts.append(file)

        return sorted(scripts)

    def scan_py_json(self):

        scripts = []

        py_json = self.root / "py-json"

        if py_json.exists():

            for file in py_json.rglob("*.py"):

                scripts.append(file)

        return sorted(scripts)