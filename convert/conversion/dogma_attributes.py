import json
import yaml

import esf_pb2

from google.protobuf.json_format import MessageToJson


def convert(path, data, patches):
    print("Loading dogmaAttributes ...")

    try:
        with open(f"{path}/dogmaAttributes.yaml") as fp:
            dogmaAttributes = yaml.load(fp, Loader=yaml.CSafeLoader)
    except FileNotFoundError:
        with open(f"{path}/dogmaattributes.json") as fp:
            dogmaAttributes = json.load(fp)
            dogmaAttributes = {int(k): v for k, v in dogmaAttributes.items()}

    data["dogmaAttributes"] = dogmaAttributes
    yield

    print("Converting dogmaAttributes ...")

    pb2 = esf_pb2.DogmaAttributes()

    for id, entry in dogmaAttributes.items():
        pb2.entries[id].name = entry["name"]
        pb2.entries[id].published = entry["published"]
        pb2.entries[id].defaultValue = entry["defaultValue"]
        pb2.entries[id].highIsGood = entry["highIsGood"]
        pb2.entries[id].stackable = entry["stackable"]

    with open("dist/sde/dogmaAttributes.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/dogmaAttributes.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))
