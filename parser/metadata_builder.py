import json

from pathlib import Path

from parser.metadata_enricher import MetadataEnricher


class MetadataBuilder:

    def __init__(self):

        with open(
            "knowledge/knowledge.json",
            encoding="utf8"
        ) as f:

            self.database = json.load(f)

        self.enricher = MetadataEnricher()

    def build(self):

        metadata = {}

        scripts = self.database["scripts"]

        total = len(scripts)

        for i, (name, script) in enumerate(
            scripts.items(),
            start=1
        ):

            print(f"[{i}/{total}] {name}")

            metadata[name] = self.enricher.enrich(
                script
            )

        Path("knowledge").mkdir(
            exist_ok=True
        )

        with open(
            "knowledge/metadata.json",
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            "\nmetadata.json generated successfully."
        )


if __name__ == "__main__":

    MetadataBuilder().build()