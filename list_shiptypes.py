import json
import os
import sys
import yaml

if len(sys.argv) < 2:
    print("Usage: python3 convert.py <path/to/eve-sde/fsd>")
    exit(1)

path = sys.argv[1]

os.makedirs("dist", exist_ok=True)

with open(f"{path}/groupIDs.yaml") as fp:
    groupIDs = yaml.load(fp, Loader=yaml.CSafeLoader)

with open(f"{path}/typeIDs.yaml") as fp:
    typeIDs = yaml.load(fp, Loader=yaml.CSafeLoader)

ships = []

for id, entry in typeIDs.items():
    group = groupIDs[entry["groupID"]]

    if group["categoryID"] == 6 and entry["published"]:
        ships.append(
            {
                "id": id,
                "name": entry["name"]["en"],
                "group": group["name"]["en"],
            }
        )

with open("dist/shiptypes.json", "w") as fp:
    json.dump(ships, fp)
