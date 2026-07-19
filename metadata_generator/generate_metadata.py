import json
from pathlib import Path

from llm import analyze

# Change these paths if necessary
KNOWLEDGE_FILE = Path("../knowledge/knowledge.json")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)


def main():

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        knowledge = json.load(f)

    total = len(knowledge)

    for index, (script_name, metadata) in enumerate(knowledge.items(), start=1):

        print(f"[{index}/{total}] {script_name}")

        script_path = metadata["path"]

        try:
            with open(script_path, "r", encoding="utf-8") as f:
                source = f.read()

        except Exception as e:
            print(f"Unable to read {script_name}")
            print(e)
            continue

        try:

            semantic = analyze(
                script_source=source,
                parser_metadata=metadata
            )

        except Exception as e:

            print(f"LLM failed on {script_name}")
            print(e)
            continue

        output_file = OUTPUT_DIR / f"{script_name}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                semantic,
                f,
                indent=4,
                ensure_ascii=False
            )

        print("Saved\n")


if __name__ == "__main__":
    main()