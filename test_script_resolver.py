import json

from agent.script_resolver import ScriptResolver

resolver = ScriptResolver()

while True:

    question = input("\nUser : ")

    if question.lower() in ["exit", "quit"]:
        break

    answer = resolver.resolve(question)

    print()

    print(json.dumps(answer, indent=4))