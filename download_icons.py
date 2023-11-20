import os
import requests
import shutil
import sys

latest = requests.get("https://binaries.eveonline.com/eveclient_TQ.json").json()
build = latest["build"]

installer = requests.get(f"https://binaries.eveonline.com/eveonline_{build}.txt").text
for line in installer.split("\n"):
    if line.startswith("app:/resfileindex.txt"):
        resfileindex = line.split(",")[1]

resfile = requests.get(f"https://binaries.eveonline.com/{resfileindex}").text

for line in resfile.split("\n"):
    if not line:
        continue

    res, path, _, _, _ = line.split(",")

    if res.startswith("res:/ui/texture/classes/fitting/"):
        filename = res.split(":")[1][1:]
        print(f"Downloading {filename} ...")
        local_path = "dist/" + filename

        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(requests.get(f"https://binaries.eveonline.com/{path}").content)
