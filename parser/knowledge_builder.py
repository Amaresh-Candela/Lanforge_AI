import json
from pathlib import Path

from parser.repository_scanner import RepositoryScanner
from parser.analyzer import ScriptAnalyzer


class KnowledgeBuilder:

    def __init__(self, repo_root):

        self.repo_root = repo_root

        self.scanner = RepositoryScanner(repo_root)

        self.analyzer = ScriptAnalyzer()

    def build(self):

        scripts = self.scanner.scan_py_scripts()

        database = {

            "repository": self.repo_root,

            "total_scripts": len(scripts),

            "scripts": {}

        }

        for script in scripts:

            print(f"Analyzing {script.name}")

            try:

                data = self.analyzer.analyze(script)

            except Exception as e:

                print(e)

                continue

            database["scripts"][script.name] = {

                "name": script.name,

                "path": str(script),

                **data

            }

        Path("knowledge").mkdir(exist_ok=True)

        with open(

            "knowledge/knowledge.json",

            "w",

            encoding="utf8"

        ) as f:

            json.dump(

                database,

                f,

                indent=4,

                ensure_ascii=False

            )

        print("\nKnowledge database generated successfully.")