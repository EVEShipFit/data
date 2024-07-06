import json
import yaml

import esf_pb2

from google.protobuf.json_format import MessageToJson


def convert(path, data):
    print("Loading marketGroups ...")

    try:
        with open(f"{path}/marketGroups.yaml") as fp:
            marketGroups = yaml.load(fp, Loader=yaml.CSafeLoader)
    except FileNotFoundError:
        with open(f"{path}/marketgroups.json") as fp:
            marketGroups = json.load(fp)
            marketGroups = {int(k): v for k, v in marketGroups.items()}

    data["marketGroups"] = marketGroups
    yield

    print("Converting marketGroups ...")

    pb2 = esf_pb2.MarketGroups()

    for id, entry in marketGroups.items():
        pb2.entries[id].name = entry["nameID"] if isinstance(entry["nameID"], str) else entry["nameID"]["en"]

        if "parentGroupID" in entry:
            pb2.entries[id].parentGroupID = entry["parentGroupID"]
        if "iconID" in entry:
            pb2.entries[id].iconID = entry["iconID"]

    with open("dist/sde/marketGroups.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/marketGroups.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))
