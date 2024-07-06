import json
import yaml

import esf_pb2

from google.protobuf.json_format import MessageToJson


def convert(path, data):
    print("Loading types ...")

    try:
        with open(f"{path}/types.yaml") as fp:
            types = yaml.load(fp, Loader=yaml.CSafeLoader)
            for type in types.values():
                type["name"] = type["name"]["en"]
    except FileNotFoundError:
        with open(f"{path}/types.json") as fp:
            types = json.load(fp)
            types = {int(k): v for k, v in types.items()}
            for type in types.values():
                type["name"] = type["typeNameID"]

    data["types"] = types
    yield

    print("Converting types ...")

    pb2 = esf_pb2.Types()

    for id, entry in types.items():
        pb2.entries[id].name = entry["name"]
        pb2.entries[id].groupID = entry["groupID"]
        pb2.entries[id].categoryID = data["groups"][entry["groupID"]]["categoryID"]
        pb2.entries[id].published = entry["published"]

        if "factionID" in entry:
            pb2.entries[id].factionID = entry["factionID"]
        if "marketGroupID" in entry:
            pb2.entries[id].marketGroupID = entry["marketGroupID"]
        if "metaGroupID" in entry:
            pb2.entries[id].metaGroupID = int(entry["metaGroupID"])
        if "capacity" in entry and entry["capacity"] != 0.0:
            pb2.entries[id].capacity = entry["capacity"]
        if "mass" in entry and entry["mass"] != 0.0:
            pb2.entries[id].mass = entry["mass"]
        if "radius" in entry and entry["radius"] != 1.0:
            pb2.entries[id].radius = entry["radius"]
        if "volume" in entry and entry["volume"] != 0.0:
            pb2.entries[id].volume = entry["volume"]

    with open("dist/sde/types.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/types.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))
