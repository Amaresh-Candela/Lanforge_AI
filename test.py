import json

with open("knowledge/knowledge.json", encoding="utf-8") as f:
    k = json.load(f)

print(type(k))
print(k.keys())