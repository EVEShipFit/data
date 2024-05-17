import os
import requests

# Only download these loaders and their data.
LOADER_LIST = [
    "categories",
    "dogmaattributes",
    "dogmaeffects",
    "iconids",
    "groups",
    "marketgroups",
    "metagroups",
    "typedogma",
    "types",
]

os.makedirs("pyd")
os.makedirs("data")

session = requests.Session()

# Find the latest installer listing.
latest = session.get("https://binaries.eveonline.com/eveclient_TQ.json").json()
build = latest["build"]
installer = session.get("https://binaries.eveonline.com/eveonline_" + build + ".txt").text

# Download all the loaders.
resfileindex = None
for line in installer.split("\n"):
    if not line:
        continue

    res, path, _, _, _, _ = line.split(",")
    if res == "app:/resfileindex.txt":
        resfileindex = line.split(",")[1]

    if not res.startswith("app:/bin64") or not res.endswith("Loader.pyd"):
        continue
    loader = res.split("/")[-1][:-10].lower()
    if loader not in LOADER_LIST:
        continue

    local_path = "pyd/" + res.split("/")[-1]

    print("Downloading " + local_path + " ...")

    with open(local_path, "wb") as f:
        f.write(session.get("https://binaries.eveonline.com/" + path).content)

if resfileindex is None:
    raise Exception("resfileindex not found")

# Download all the fsdbinary files.
resfile = requests.get("https://binaries.eveonline.com/" + resfileindex).text
for line in resfile.split("\n"):
    if not line:
        continue

    res, path, _, _, _ = line.split(",")
    if (
        not res.startswith("res:/staticdata/") or not res.endswith(".fsdbinary")
    ) and res != "res:/localizationfsd/localization_fsd_en-us.pickle":
        continue
    loader = res.split("/")[-1][:-10]
    if res != "res:/localizationfsd/localization_fsd_en-us.pickle" and loader not in LOADER_LIST:
        continue

    local_path = "data/" + res.split("/")[-1]

    print("Downloading " + local_path + " ...")

    with open(local_path, "wb") as f:
        f.write(session.get("https://resources.eveonline.com/" + path).content)
