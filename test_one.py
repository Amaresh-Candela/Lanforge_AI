import json
from pathlib import Path

from metadata_generator.llm import analyze

# Change this if your knowledge.json is elsewhere
KNOWLEDGE_FILE = Path("knowledge/knowledge.json")


def main():

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        knowledge = json.load(f)

    SCRIPT_NAME = "lf_dataplane_test.py"

    if SCRIPT_NAME not in knowledge["scripts"]:
        print(f"{SCRIPT_NAME} not found.")
        return

    metadata = knowledge["scripts"][SCRIPT_NAME]

    script_path = Path(metadata["path"])

    print("=" * 80)
    print("Reading Script")
    print("=" * 80)
    print(script_path)

    with open(script_path, "r", encoding="utf-8") as f:
        source = f.read()

    print(f"\nLoaded {len(source)} characters\n")

    print("=" * 80)
    print("Sending to GPT...")
    print("=" * 80)

    result = analyze(
        script_source=source,
        parser_metadata=metadata
    )

    print("=" * 80)
    print("LLM Response")
    print("=" * 80)

    print(json.dumps(result, indent=4, ensure_ascii=False))

    output = Path("metadata_generator/output")
    output.mkdir(exist_ok=True)

    output_file = output / f"{SCRIPT_NAME}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("\nSaved to:")
    print(output_file)


if __name__ == "__main__":
    main()