import json
import yaml

import esf_pb2

from google.protobuf.json_format import MessageToJson


def convert(path, data):
    print("Loading categories ...")

    try:
        with open(f"{path}/categories.yaml") as fp:
            categories = yaml.load(fp, Loader=yaml.CSafeLoader)
            for category in categories.values():
                category["name"] = category["name"]["en"]
    except FileNotFoundError:
        with open(f"{path}/categories.json") as fp:
            categories = json.load(fp)
            categories = {int(k): v for k, v in categories.items()}
            for category in categories.values():
                category["name"] = category["categoryNameID"]

    data["categories"] = categories
    yield

    print("Converting categories ...")

    pb2 = esf_pb2.Categories()

    for id, entry in categories.items():
        pb2.entries[id].name = entry["name"]
        pb2.entries[id].published = entry["published"]

    with open("dist/sde/categories.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/categories.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))
