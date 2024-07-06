import json
import yaml

import esf_pb2

from google.protobuf.json_format import MessageToJson


def convert(path, data):
    print("Loading groups ...")

    try:
        with open(f"{path}/groups.yaml") as fp:
            groups = yaml.load(fp, Loader=yaml.CSafeLoader)
            for group in groups.values():
                group["name"] = group["name"]["en"]
    except FileNotFoundError:
        with open(f"{path}/groups.json") as fp:
            groups = json.load(fp)
            groups = {int(k): v for k, v in groups.items()}
            for group in groups.values():
                group["name"] = group["groupNameID"]

    data["groups"] = groups
    yield

    print("Converting groups ...")

    pb2 = esf_pb2.Groups()

    for id, entry in groups.items():
        pb2.entries[id].name = entry["name"]
        pb2.entries[id].categoryID = entry["categoryID"]
        pb2.entries[id].published = entry["published"]

    with open("dist/sde/groups.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/groups.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))
