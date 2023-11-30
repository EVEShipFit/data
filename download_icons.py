import os
import requests

folders = [
    "res:/ui/texture/classes/fitting",
    "res:/ui/texture/classes/fitting/statsicons",
    "res:/ui/texture/shared",
    "res:/ui/texture/windowicons",
]


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

    dirname = os.path.dirname(res)

    if res.endswith(".png") and dirname in folders:
        filename = res.split(":")[1][1:]
        print(f"Downloading {filename} ...")
        local_path = "dist/" + filename

        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(session.get(f"https://resources.eveonline.com/{path}").content)
