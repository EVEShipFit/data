import os
import sys
import yaml
import json

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
    name = entry["name"]["en"]
    groupID = entry["groupID"]
    published = entry["published"]

    group = groupIDs[entry["groupID"]]
    groupName = group["name"]["en"]
    categoryID = group["categoryID"]

    if categoryID == 6 and published:
        ships.append(
            {
                "id": id,
                "name": name,
                "group": groupName,
            }
        )

with open("dist/ships.json", "w") as fp:
    json.dump(ships, fp)
