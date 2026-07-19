from pathlib import Path


class RepositoryCrawler:

    def crawl(self, root):

        files = []

        root = Path(root)

        for file in root.rglob("*.py"):

            files.append(str(file))

        return sorted(files)