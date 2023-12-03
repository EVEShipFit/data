import os
import requests
import sys
import yaml

if len(sys.argv) < 2:
    print("Usage: python3 download_icons.py <path/to/eve-sde/fsd>")
    exit(1)

path = sys.argv[1]

folders = [
    "res:/ui/texture/classes/fitting",
    "res:/ui/texture/classes/fitting/statsicons",
    "res:/ui/texture/shared",
    "res:/ui/texture/windowicons",
]
files = {}

with open(f"{path}/marketGroups.yaml") as fp:
    marketGroups = yaml.load(fp, Loader=yaml.CSafeLoader)

with open(f"{path}/metaGroups.yaml") as fp:
    metaGroups = yaml.load(fp, Loader=yaml.CSafeLoader)

with open(f"{path}/iconIDs.yaml") as fp:
    iconIDs = yaml.load(fp, Loader=yaml.CSafeLoader)

for marketGroupID, marketGroup in marketGroups.items():
    if "iconID" not in marketGroup or marketGroup["iconID"] == 0:
        continue

    # Avatar related icons
    topParentGroupID = marketGroupID
    while "parentGroupID" in marketGroups[topParentGroupID]:
        topParentGroupID = marketGroups[topParentGroupID]["parentGroupID"]
    if topParentGroupID == 1396:
        continue

    filename = iconIDs[marketGroup["iconID"]]["iconFile"].lower()
    files[filename] = f"icons/{marketGroup['iconID']}"

for metaGroup in metaGroups.values():
    if "iconID" not in metaGroup or metaGroup["iconID"] == 0:
        continue

    filename = iconIDs[metaGroup["iconID"]]["iconFile"].lower()
    files[filename] = f"icons/{metaGroup['iconID']}"

latest = requests.get("https://binaries.eveonline.com/eveclient_TQ.json").json()
build = latest["build"]

installer = requests.get(f"https://binaries.eveonline.com/eveonline_{build}.txt").text
for line in installer.split("\n"):
    if line.startswith("app:/resfileindex.txt"):
        resfileindex = line.split(",")[1]

resfile = requests.get(f"https://binaries.eveonline.com/{resfileindex}").text

session = requests.Session()

for line in resfile.split("\n"):
    if not line:
        continue

    res, path, _, _, _ = line.split(",")
    if not res.endswith(".png"):
        continue

    dirname = os.path.dirname(res)
    if dirname not in folders and res not in files:
        continue

    filename = res.split(":")[1][1:]

    if dirname in folders:
        local_path = filename
    else:
        local_path = files[res] + ".png"

    print(f"Downloading {filename} to {local_path} ...")
    local_path = f"dist/{local_path}"

    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(session.get(f"https://resources.eveonline.com/{path}").content)
