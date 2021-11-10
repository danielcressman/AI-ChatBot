import json
import typing

with open("intents.json") as file:
    data = json.load(file)

output: typing.Dict[str, typing.List[str]] = {}
for intent in data["intents"]:
    output[intent['tag']] = []

with open("extra_patterns.json", "w") as outfile:
    json.dump(output, outfile, indent=2)
