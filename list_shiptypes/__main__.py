import json
import os
import sys
import yaml

if len(sys.argv) < 2:
    print("Usage: python3 convert.py <path/to/eve-sde/fsd>")
    exit(1)

path = sys.argv[1]

os.makedirs("dist", exist_ok=True)

try:
    with open(f"{path}/groupIDs.yaml") as fp:
        groupIDs = yaml.load(fp, Loader=yaml.CSafeLoader)
except FileNotFoundError:
    with open(f"{path}/groups.json") as fp:
        groupIDs = json.load(fp)
        groupIDs = {int(k): v for k, v in groupIDs.items()}

try:
    with open(f"{path}/typeIDs.yaml") as fp:
        typeIDs = yaml.load(fp, Loader=yaml.CSafeLoader)
except FileNotFoundError:
    with open(f"{path}/types.json") as fp:
        typeIDs = json.load(fp)
        typeIDs = {int(k): v for k, v in typeIDs.items()}

ships = []

for id, entry in typeIDs.items():
    group = groupIDs[entry["groupID"]]

    if group["categoryID"] == 6 and entry["published"]:
        ships.append(
            {
                "id": id,
                "name": entry["name"]["en"] if "name" in entry else entry["typeNameID"],
                "group": group["name"]["en"] if "name" in group else group["groupNameID"],
            }
        )

with open("dist/shiptypes.json", "w") as fp:
    json.dump(ships, fp)
